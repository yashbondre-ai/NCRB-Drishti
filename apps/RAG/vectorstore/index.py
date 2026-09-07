import os
import json
import numpy as np

from .faiss_store import FAISSStore

class VectorIndexer:

    def __init__(self):
        self.store = FAISSStore()
        self.index = self.store.get_index()

        self.metadata_path = "apps/RAG/vectorstore_data/metadata.json"

    def add_embedding(self, embedding, metadata):
        """
        Add a single embedding vector (or a batch of them) to the index.

        If a 2D array (batch) is passed, each row is added as its own vector.
        """
        embedding = np.asarray(embedding, dtype="float32")

        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)

        self._validate_dimension(embedding)

        start_id = self.index.ntotal
        self.index.add(embedding)
        self.store.save_index()

        # Save metadata once for all added vectors (one row == one vector)
        all_metadata = self._load_all_metadata()
        for i in range(embedding.shape[0]):
            all_metadata[str(start_id + i)] = metadata
        self._write_all_metadata(all_metadata)

    def save_metadata(self, vector_id, metadata):
        all_metadata = self._load_all_metadata()
        all_metadata[str(vector_id)] = metadata
        self._write_all_metadata(all_metadata)

    def _validate_dimension(self, embeddings):
        """Ensure embedding dimension matches the FAISS index dimension."""
        if embeddings.ndim == 1:
            dim = embeddings.shape[0]
        else:
            dim = embeddings.shape[1]

        if dim != self.store.dimension:
            raise ValueError(
                f"Embedding dimension {dim} does not match index dimension "
                f"{self.store.dimension}."
            )

    def _load_all_metadata(self):
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def _write_all_metadata(self, all_metadata):
        folder_path = os.path.dirname(self.metadata_path)

        if folder_path and not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)

        with open(self.metadata_path, "w", encoding="utf-8") as file:
            json.dump(all_metadata, file, indent=4, ensure_ascii=False)

    def add_embeddings(self, embeddings: np.ndarray, metadata_list: list):
        """
        Add multiple embeddings and their metadata.

        metadata.json is written only ONCE after all vectors are inserted,
        avoiding a full-file rewrite for every single chunk.
        """

        # Convert to float32 (required by FAISS); asarray avoids a copy
        # when the array is already float32.
        embeddings = np.asarray(embeddings, dtype=np.float32)

        self._validate_dimension(embeddings)

        # Get starting vector ID
        start_id = self.index.ntotal

        # Add all embeddings at once
        self.index.add(embeddings)

        # Save updated FAISS index
        self.store.save_index()

        # Load existing metadata once, merge all new records, write once
        all_metadata = self._load_all_metadata()
        for i, metadata in enumerate(metadata_list):
            all_metadata[str(start_id + i)] = metadata
        self._write_all_metadata(all_metadata)

        return list(range(start_id, start_id + len(metadata_list)))

    def get_total_vectors(self):
        return self.index.ntotal

