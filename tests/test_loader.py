import pytest
import spacy

from ..modules import loader
from ..modules import formatter


filepath = "tests/test.txt"
loader = loader.SentenceLoader(formatter.DistanceFormatter(), filepath)


def test_loadertype():
    for sentence in loader:
        if sentence:
            assert isinstance(sentence[0], spacy.tokens.Token)


def test_loaderlines():
    with open(filepath) as f:
        lines = f.readlines()
    line_length = len(lines)
    loader_length = len([l for l in loader])
    assert loader_length == line_length
