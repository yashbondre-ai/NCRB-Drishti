import json
import os

import numpy as np

from .faiss_store import FAISSStore


def search(query_embedding, top_k=5):
    """
    Retrieve the top-k most similar vectors from the FAISS index.

    Args:
        query_embedding: A single embedding vector (1D numpy array/list) or a
            batch of embeddings (2D array).
        top_k: Number of neighbours to retrieve.

    Returns:
        A list of dicts, each with:
            - id: vector id in the index
            - distance: FAISS L2 distance (lower is more similar)
            - metadata: stored metadata dict for that vector
            - chunk_text: the text chunk (metadata["chunk_text"])
    """
    store = FAISSStore()
    index = store.get_index()

    if index.ntotal == 0:
        return []

    # Normalize the query embedding to a 2D float32 array (required by FAISS).
    query_embedding = np.asarray(query_embedding, dtype="float32")
    if query_embedding.ndim == 1:
        query_embedding = query_embedding.reshape(1, -1)

    if query_embedding.shape[1] != store.dimension:
        raise ValueError(
            f"Query embedding dimension {query_embedding.shape[1]} does not "
            f"match index dimension {store.dimension}."
        )

    k = min(top_k, index.ntotal)
    distances, indices = index.search(query_embedding, k)

    metadata = _load_metadata()

    results = []
    for distance, vector_id in zip(distances[0], indices[0]):
        if vector_id == -1:
            continue

        record = metadata.get(str(vector_id), {})
        results.append(
            {
                "id": int(vector_id),
                "distance": float(distance),
                "metadata": record,
                "chunk_text": record.get("chunk_text") or record.get("text", ""),
            }
        )

    return results


def _load_metadata():
    metadata_path = "apps/RAG/vectorstore_data/metadata.json"
    if os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}
