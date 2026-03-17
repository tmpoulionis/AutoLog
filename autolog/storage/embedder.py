from sentence_transformers import SentenceTransformer

import autolog.config as config


class Embedder:
    def __init__(self, model_name: str | None = None) -> None:
        self._model = SentenceTransformer(model_name or config.EMBEDDING_MODEL)

    def embed(self, text: str) -> list[float]:
        """Return a 384-dim embedding vector for a single string."""
        return self._model.encode(text, convert_to_numpy=True).tolist()
