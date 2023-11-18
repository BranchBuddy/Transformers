import pytest
import time

from src.OpenaiHandler import OpenAiHandler

CODE = "def add(a, b):\n    return a + b"


@pytest.fixture
def openai_handler():
    return OpenAiHandler()
