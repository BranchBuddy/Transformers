import pytest
from src.Digester import Digester

@pytest.fixture
def commit_message():
    with open('tests/resources/commits.message', 'r', encoding='utf-8') as f:
        return f.read()

@pytest.fixture
def diff_message():
    with open('tests/resources/diff.message', 'r', encoding='utf-8') as f:
        return f.read()

@pytest.fixture
def digester():
    return Digester()

def test_digester(digester, commit_message, diff_message):
    response = digester.digest(commit_message, diff_message, 'daily')
    digest = response['response']
    assert len(digest) > 20, "A resonable digest should be longer than 20 characters."
