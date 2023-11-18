import pytest
import time

from src.openai_handler import OpenAiHandler

CODE = "def add(a, b):\n    return a + b"


@pytest.fixture
def openai_handler():
    return OpenAiHandler()

def test_summarize_code(openai_handler):
    start = time.time()
    res = openai_handler.summarize_code(CODE)
    end = time.time()
    assert 'sum' in res
    print(res)
    print(f"Time taken: {end - start} seconds")
