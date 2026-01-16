from sentence_transformers import SentenceTransformer, util

class SemanticEvaluator:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def similarity(self, q: str, a: str) -> float:
        embeddings = self.model.encode([q, a], convert_to_tensor=True)
        score = util.cos_sim(embeddings[0], embeddings[1])
        return float(score) * 10  # scale to 0–10
