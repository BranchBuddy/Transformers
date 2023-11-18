import time
import requests
from openai import OpenAI
from src.OpenaiHandler import OpenAiHandler

class CodeSummarizer:


    def __init__(self):
        self.handler = OpenAiHandler()
    
    
    def summarize_code(self, code_snippet: str) -> str:
        """
        Summarizes the functionality of a given code snippet using OpenAI's text-davinci-003 model.

        Args:
            code_snippet (str): The code snippet to be summarized.

        Returns:
            str: The summarized description of the code snippet.
        """
        response = self.handler.client.completions.create(
            model="text-davinci-003",
            prompt=f"Here is a code snippet:\n\n{code_snippet}\n\nSummarize what this code does:",
            max_tokens=1000,
            temperature=0.7,
            n=1,
            stop=None
        )
        return response.choices[0].text.strip()

    def summarizeCode(self, code: str):
        # This code is for v1 of the openai package: pypi.org/project/openai
        self.handler.createAssistant('summary')
        response = self.handler.handleTask('summary',code)
        return response