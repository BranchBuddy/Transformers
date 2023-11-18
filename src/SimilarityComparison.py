import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from scipy.spatial.distance import cosine


class SimilarityComparison:

    def __init__(self) -> None:
        # Load BERT model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        self.model = AutoModel.from_pretrained("microsoft/codebert-base")
    
    def get_bert_embedding(self, code):
        """
        Get the BERT embedding for the given code.

        Args:
            code (str): The code to be embedded.

        Returns:
            numpy.ndarray: The BERT embedding of the code.
        """
        embedding = self.tokenizer.encode(code, return_tensors="pt")
        with torch.no_grad():
            embedding = self.model(embedding).last_hidden_state.mean(dim=1).numpy()
        return embedding

    def calculate_cosine_similarity(self, embedding1, embedding2):
        """
        Calculates the cosine similarity between two embeddings.

        Parameters:
        embedding1 (numpy.ndarray): The first embedding.
        embedding2 (numpy.ndarray): The second embedding.

        Returns:
        float: The cosine similarity between the two embeddings.
        """
        return 1 - cosine(embedding1, embedding2)


    def compare(self, code1, code2):
        """
        Compare the similarity between two code snippets.

        Args:
            code1 (str): The first code snippet.
            code2 (str): The second code snippet.

        Returns:
            float: The similarity score between the two code snippets.
        """
        embedding1 = self.get_bert_embedding(code1)[0]
        embedding2 = self.get_bert_embedding(code2)[0]
        similarity_score = self.calculate_cosine_similarity(embedding1, embedding2)
        return similarity_score

    def compare_functions(self, focused_functions: list, other_functions: list):
        """
        Compare the similarity between a list of focused functions and a list of other functions.

        Args:
            focused_functions (list): A list of focused functions to compare.
            other_functions (list): A list of other functions to compare against.

        Returns:
            np.ndarray: A 2D array of similarity scores between the focused functions and other functions.
        """
        similarities = np.zeros((len(focused_functions), len(other_functions)))
        for i, focused_function in enumerate(focused_functions):
            for j, other_function in enumerate(other_functions):
                similarity_score = self.compare(focused_function, other_function)
                similarities[i, j] = similarity_score
        return similarities

    def get_similar_functions(self, focused_functions: list, other_functions: list, threshold: float = 0.9):
        """
        Get the indices and similarities of functions that are similar to the focused functions.

        Args:
            focused_functions (list): List of focused functions to compare.
            other_functions (list): List of other functions to compare against.
            threshold (float, optional): Similarity threshold. Functions with similarity above this threshold will be considered similar. Defaults to 0.9.

        Returns:
            list: List of tuples containing the indices and similarities of similar functions.
        """
        similarities = self.compare_functions(focused_functions, other_functions)
        indices_with_similarity = [(i, j, similarities[i, j]) for i, j in zip(*np.where(similarities > threshold))]
        return indices_with_similarity
