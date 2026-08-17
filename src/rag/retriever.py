from typing import List, Dict, Any, Optional
from src.vectorstore.store_manager import VectorStoreManager

class MultimodalRetriever:
    """
    Multimodal Context Retriever wrapping VectorStoreManager.
    Filters and ranks document chunks based on semantic relevance and layout metadata.
    """
    def __init__(self, vector_store: VectorStoreManager, top_k: int = 4):
        self.vector_store = vector_store
        self.top_k = top_k

    def get_relevant_documents(self, query: str, filter_doc: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves top_k relevant context chunks for given user query.
        """
        if not query.strip():
            return []

        results = self.vector_store.similarity_search(
            query=query,
            top_k=self.top_k,
            filter_doc=filter_doc
        )
        return results
