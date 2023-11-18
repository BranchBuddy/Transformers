from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine


class SimilarityComparison:

    def __init__(self) -> None:
        # Load BERT model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        self.model = AutoModel.from_pretrained("microsoft/codebert-base")
    
    def get_bert_embedding(self, code):
        embedding = self.tokenizer.encode(code, return_tensors="pt")
        with torch.no_grad():
            embedding = self.model(embedding).last_hidden_state.mean(dim=1).numpy()
        return embedding

    def calculate_cosine_similarity(self, embedding1, embedding2):
        return 1 - cosine(embedding1, embedding2)


    def compare(self, code1, code2):
        embedding1 = self.get_bert_embedding(code1)[0]
        
        embedding2 = self.get_bert_embedding(code2)[0]

        similarity_score = self.calculate_cosine_similarity(embedding1, embedding2)
        return similarity_score