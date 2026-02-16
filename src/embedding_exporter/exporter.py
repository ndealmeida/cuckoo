import logging
import os
from typing import List

from injector import inject, singleton
from sentence_transformers import SentenceTransformer

from src.config import Config

logger = logging.getLogger(__name__)

# Silence the specific "LOAD REPORT" and other model-loading noise from transformers
# This won't hide download progress from huggingface_hub if it happens
logging.getLogger("transformers").setLevel(logging.ERROR)


@singleton
class EmbeddingExporter:
    @inject
    def __init__(self, config: Config):
        model_name = config.embedding.model_name
        cache_folder = config.embedding.cache_folder

        # Check if model is already cached to avoid network HEAD requests
        local_files_only = False
        if os.path.exists(cache_folder) and os.listdir(cache_folder):
            local_files_only = True

        try:
            self.model = SentenceTransformer(
                model_name,
                cache_folder=cache_folder,
                local_files_only=local_files_only
            )
        except Exception:
            # Fallback to online if local load fails
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
