import os
from dotenv import load_dotenv
from openai import OpenAI

class OpenAiHandler:
    """
    A class that handles interactions with OpenAI's text-davinci-003 model for code summarization.
    """

    def __init__(self) -> None:
        """
        Initializes the OpenAiHandler class.

        Loads the OpenAI API key from the environment variables and creates an instance of the OpenAI class.
        """
        load_dotenv()
        openai_key = os.getenv("OPENAI_KEY")
        self.openai = OpenAI(api_key=openai_key)

    def summarize_code(self, code_snippet: str) -> str:
        """
        Summarizes the functionality of a given code snippet using OpenAI's text-davinci-003 model.

        Args:
            code_snippet (str): The code snippet to be summarized.

        Returns:
            str: The summarized description of the code snippet.
        """
        response = self.openai.completions.create(
            model="text-davinci-003",
            prompt=f"Here is a code snippet:\n\n{code_snippet}\n\nSummarize what this code does:",
            max_tokens=1000,
            temperature=0.7,
            n=1,
            stop=None
        )
        return response.choices[0].text.strip()
