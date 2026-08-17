import math
import hashlib
import re
from typing import List
from config.settings import get_settings

class BaseEmbeddingWrapper:
    """
    Embedding interface producing dense vector representations.
    Supports HuggingFace, OpenAI, and deterministic hash embeddings for testing.
    """
    def __init__(self, provider: str = None, model_name: str = None):
        self.settings = get_settings()
        self.provider = provider or self.settings.embedding_provider
        self.model_name = model_name or (
            self.settings.openai_embedding_model if self.provider == "openai" else self.settings.hf_model_name
        )
        self.dimension = 384 if "MiniLM" in self.model_name or "bge-small" in self.model_name else 1536
        self._init_model()

    def _init_model(self):
        self.engine = None
        if self.provider == "openai" and self.settings.openai_api_key:
            try:
                from langchain_openai import OpenAIEmbeddings
                self.engine = OpenAIEmbeddings(
                    model=self.model_name,
                    api_key=self.settings.openai_api_key
                )
            except Exception:
                pass
        elif self.provider == "huggingface":
            try:
                from langchain_community.embeddings import HuggingFaceEmbeddings
                self.engine = HuggingFaceEmbeddings(model_name=self.model_name)
            except Exception:
                pass

    def embed_query(self, text: str) -> List[float]:
        """Embeds a single query string into a vector."""
        if self.engine:
            try:
                return self.engine.embed_query(text)
            except Exception:
                pass

        return self._generate_deterministic_vector(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embeds a list of document strings into vectors."""
        if self.engine:
            try:
                return self.engine.embed_documents(texts)
            except Exception:
                pass

        return [self._generate_deterministic_vector(t) for t in texts]

    def _generate_deterministic_vector(self, text: str) -> List[float]:
        """Fallback dense vector embedding with keyword token overlap encoding."""
        words = set(re.findall(r'\w+', text.lower()))
        vector = []
        for i in range(self.dimension):
            h = hashlib.sha256(f"dim_{i}".encode('utf-8')).hexdigest()
            feature_word = h[:8]
            # Check if any word in text hashes to feature
            match_score = sum(1.0 for w in words if hashlib.md5(w.encode('utf-8')).hexdigest()[:4] == h[:4])
            val = (int(h[:6], 16) / 0xFFFFFF) * 0.1 + match_score * 2.0
            vector.append(val)
        
        # Normalize
        norm = math.sqrt(sum(v * v for v in vector))
        return [v / norm for v in vector] if norm > 0 else vector

def get_embedding_function(provider: str = None, model_name: str = None) -> BaseEmbeddingWrapper:
    return BaseEmbeddingWrapper(provider=provider, model_name=model_name)
