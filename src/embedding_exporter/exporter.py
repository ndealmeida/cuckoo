import logging
from typing import List

from injector import inject, singleton
from sentence_transformers import SentenceTransformer

from src.config import Config

logger = logging.getLogger(__name__)


@singleton
class EmbeddingExporter:
    @inject
    def __init__(self, config: Config):
        model_name = config.embedding.model_name
        cache_folder = config.embedding.cache_folder
        self.model = SentenceTransformer(model_name, cache_folder=cache_folder)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def encode(self, text: str) -> List[float]:
        """Convert a string into a list of floats (vector)."""
        embedding = self.model.encode(text)
        return embedding.tolist()

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Convert a list of strings into a list of vectors."""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
