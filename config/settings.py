import os
from dataclasses import dataclass, field
from typing import Optional

try:
    from pydantic_settings import BaseSettings
    from pydantic import Field

    class Settings(BaseSettings):
        openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
        openai_model_name: str = Field(default="gpt-4o-mini", env="OPENAI_MODEL_NAME")
        openai_embedding_model: str = Field(default="text-embedding-3-small", env="OPENAI_EMBEDDING_MODEL")
        
        vector_store_provider: str = Field(default="chroma", env="VECTOR_STORE_PROVIDER")
        chroma_persist_directory: str = Field(default="./data/chroma_db", env="CHROMA_PERSIST_DIRECTORY")
        pinecone_api_key: str = Field(default="", env="PINECONE_API_KEY")
        pinecone_environment: str = Field(default="us-east-1", env="PINECONE_ENVIRONMENT")
        pinecone_index_name: str = Field(default="multimodal-doc-intelligence", env="PINECONE_INDEX_NAME")
        
        embedding_provider: str = Field(default="huggingface", env="EMBEDDING_PROVIDER")
        hf_model_name: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", env="HF_MODEL_NAME")
        
        langchain_tracing_v2: bool = Field(default=True, env="LANGCHAIN_TRACING_V2")
        langchain_api_key: str = Field(default="", env="LANGCHAIN_API_KEY")
        langchain_project: str = Field(default="multimodal-document-intelligence", env="LANGCHAIN_PROJECT")
        
        enable_pii_masking: bool = Field(default=True, env="ENABLE_PII_MASKING")
        enable_prompt_injection_scanner: bool = Field(default=True, env="ENABLE_PROMPT_INJECTION_SCANNER")
        confidence_threshold: float = Field(default=0.65, env="CONFIDENCE_THRESHOLD")

        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"

except ImportError:
    @dataclass
    class Settings:
        openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
        openai_model_name: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini"))
        openai_embedding_model: str = field(default_factory=lambda: os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
        
        vector_store_provider: str = field(default_factory=lambda: os.getenv("VECTOR_STORE_PROVIDER", "chroma"))
        chroma_persist_directory: str = field(default_factory=lambda: os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db"))
        pinecone_api_key: str = field(default_factory=lambda: os.getenv("PINECONE_API_KEY", ""))
        pinecone_environment: str = field(default_factory=lambda: os.getenv("PINECONE_ENVIRONMENT", "us-east-1"))
        pinecone_index_name: str = field(default_factory=lambda: os.getenv("PINECONE_INDEX_NAME", "multimodal-doc-intelligence"))
        
        embedding_provider: str = field(default_factory=lambda: os.getenv("EMBEDDING_PROVIDER", "huggingface"))
        hf_model_name: str = field(default_factory=lambda: os.getenv("HF_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"))
        
        langchain_tracing_v2: bool = field(default_factory=lambda: os.getenv("LANGCHAIN_TRACING_V2", "true").lower() == "true")
        langchain_api_key: str = field(default_factory=lambda: os.getenv("LANGCHAIN_API_KEY", ""))
        langchain_project: str = field(default_factory=lambda: os.getenv("LANGCHAIN_PROJECT", "multimodal-document-intelligence"))
        
        enable_pii_masking: bool = field(default_factory=lambda: os.getenv("ENABLE_PII_MASKING", "true").lower() == "true")
        enable_prompt_injection_scanner: bool = field(default_factory=lambda: os.getenv("ENABLE_PROMPT_INJECTION_SCANNER", "true").lower() == "true")
        confidence_threshold: float = field(default_factory=lambda: float(os.getenv("CONFIDENCE_THRESHOLD", "0.65")))

_settings_instance: Optional[Settings] = None

def get_settings() -> Settings:
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
