from sentence_transformers import SentenceTransformer, util


class SemanticEvaluator:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def similarity(self, question: str, answer: str) -> float:
        embeddings = self.model.encode([question, answer], convert_to_tensor=True)
        score = util.cos_sim(embeddings[0], embeddings[1])
        return round(float(score) * 10, 2)  # scale to 0–10
