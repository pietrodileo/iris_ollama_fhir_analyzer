from sentence_transformers import SentenceTransformer

class Transformer:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def create_vector(self, data: dict) -> dict:
        desc = data["description"]
        vector = self.model.encode(desc, normalize_embeddings=True).tolist()

        return {
            "description": desc,
            "vector": vector
        }
