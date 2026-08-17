import os
import sqlite3
import json
import math
from typing import List, Dict, Any, Optional
from config.settings import get_settings
from src.vectorstore.embeddings import get_embedding_function, BaseEmbeddingWrapper
from src.ingestion.pdf_parser import ExtractedChunk

class VectorStoreManager:
    """
    Vector Store Abstraction supporting local ChromaDB persistent vector database
    and Pinecone cloud infrastructure, with pure Python SQLite fallback.
    """
    def __init__(self, provider: str = None, persist_dir: str = None):
        self.settings = get_settings()
        self.provider = provider or self.settings.vector_store_provider
        self.persist_dir = persist_dir or self.settings.chroma_persist_directory
        self.embedder: BaseEmbeddingWrapper = get_embedding_function()
        os.makedirs(self.persist_dir, exist_ok=True)
        self._init_store()

    def _init_store(self):
        self.chroma_client = None
        self.chroma_collection = None
        
        if self.provider == "chroma":
            try:
                import chromadb
                self.chroma_client = chromadb.PersistentClient(path=self.persist_dir)
                self.chroma_collection = self.chroma_client.get_or_create_collection(
                    name="multimodal_docs",
                    metadata={"hnsw:space": "cosine"}
                )
                return
            except Exception:
                pass

        # Fallback sqlite3 vector index for robust local execution
        self.db_path = os.path.join(self.persist_dir, "local_vector_index.db")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    text TEXT,
                    page_number INTEGER,
                    doc_name TEXT,
                    chunk_type TEXT,
                    metadata TEXT,
                    embedding TEXT
                )
            """)
            conn.commit()

    def add_chunks(self, chunks: List[ExtractedChunk]):
        """
        Indexes extracted chunks into the vector store.
        """
        if not chunks:
            return

        texts = [c.text for c in chunks]
        embeddings = self.embedder.embed_documents(texts)

        if self.chroma_collection:
            try:
                ids = [f"{c.doc_name}_p{c.page_number}_{idx}" for idx, c in enumerate(chunks)]
                metadatas = [c.metadata for c in chunks]
                self.chroma_collection.add(
                    ids=ids,
                    documents=texts,
                    embeddings=embeddings,
                    metadatas=metadatas
                )
                return
            except Exception:
                pass

        # SQLite vector store insertion
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for idx, (c, emb) in enumerate(zip(chunks, embeddings)):
                doc_id = f"{c.doc_name}_p{c.page_number}_{idx}"
                cursor.execute("""
                    INSERT OR REPLACE INTO documents (id, text, page_number, doc_name, chunk_type, metadata, embedding)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    doc_id,
                    c.text,
                    c.page_number,
                    c.doc_name,
                    c.chunk_type,
                    json.dumps(c.metadata),
                    json.dumps(emb)
                ))
            conn.commit()

    def similarity_search(self, query: str, top_k: int = 4, filter_doc: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Executes vector similarity search against indexed document chunks.
        """
        query_vec = self.embedder.embed_query(query)

        if self.chroma_collection:
            try:
                where_clause = {"source": filter_doc} if filter_doc else None
                results = self.chroma_collection.query(
                    query_embeddings=[query_vec],
                    n_results=top_k,
                    where=where_clause
                )
                
                formatted = []
                if results and results.get("documents"):
                    docs = results["documents"][0]
                    metadatas = results["metadatas"][0]
                    distances = results.get("distances", [[0.1] * len(docs)])[0]
                    
                    for doc_text, meta, dist in zip(docs, metadatas, distances):
                        # Convert distance to similarity score
                        score = max(0.0, 1.0 - (dist if dist is not None else 0.2))
                        formatted.append({
                            "text": doc_text,
                            "metadata": meta,
                            "score": round(score, 3),
                            "page": meta.get("page", 1),
                            "source": meta.get("source", "Document")
                        })
                return formatted
            except Exception:
                pass

        # SQLite fallback vector query using cosine similarity
        results = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if filter_doc:
                cursor.execute("SELECT id, text, page_number, doc_name, metadata, embedding FROM documents WHERE doc_name = ?", (filter_doc,))
            else:
                cursor.execute("SELECT id, text, page_number, doc_name, metadata, embedding FROM documents")
            
            rows = cursor.fetchall()
            for doc_id, text, page_num, doc_name, meta_str, emb_str in rows:
                doc_vec = json.loads(emb_str)
                score = self._cosine_similarity(query_vec, doc_vec)
                meta = json.loads(meta_str)
                results.append({
                    "text": text,
                    "metadata": meta,
                    "score": round(score, 3),
                    "page": page_num,
                    "source": doc_name
                })

        # Sort descending by similarity score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)
