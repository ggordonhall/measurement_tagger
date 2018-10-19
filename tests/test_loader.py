import pytest
import spacy

from ..modules import loader, formatter


filepath = '..text/measurements.txt'
loader = loader.SentenceLoader(formatter.DistanceFormatter(), filepath)


def test_loadertype():
    for sentence in loader:
        assert isinstance(sentence, spacy.tokens.Span)


def test_loaderlines():
    with open(filepath) as f:
        lines = f.readlines()
    line_length = len(lines)
    loader_length = len([l for l in loader])
    assert loader_length == line_length
