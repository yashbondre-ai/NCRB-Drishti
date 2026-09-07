from .embedding_model import get_embedding_model


def generate_embeddings(chunks):

    model = get_embedding_model()

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True
    )

    return embeddings