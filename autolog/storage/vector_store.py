import chromadb

import autolog.config as config
from autolog.storage.embedder import Embedder


class VectorStore:
    def __init__(self, project_name: str, embedder: Embedder | None = None) -> None:
        self._embedder   = embedder or Embedder()
        self._client     = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
        self._collection = self._client.get_or_create_collection(name=project_name)
        self._project    = project_name

    def upsert(self, entry_id: str, text: str, timestamp: str) -> None:
        """Embed text and upsert into the collection. Idempotent on entry_id."""
        vector = self._embedder.embed(text)
        self._collection.upsert(
            ids=[entry_id],
            embeddings=[vector],
            documents=[text],
            metadatas=[{"timestamp": timestamp, "project": self._project}],
        )

    def search(self, query_text: str, top_k: int = 3) -> list[dict]:
        """Return the top-k most similar entries for a query string.

        Each result dict has keys: id, text, timestamp, distance.
        """
        count = self._collection.count()
        if count == 0:
            return []

        query_vector = self._embedder.embed(query_text)
        results = self._collection.query(
            query_embeddings=[query_vector],
            n_results=min(top_k, count),
            include=["documents", "metadatas", "distances"],
        )

        return [
            {
                "id":        entry_id,
                "text":      doc,
                "timestamp": meta["timestamp"],
                "distance":  dist,
            }
            for entry_id, doc, meta, dist in zip(
                results["ids"][0],
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]
