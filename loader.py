from typing import List

import spacy

from utils import flatten


class SentenceLoader:
    """Load and tokenise sentences from a dataset.

    Arguments:
        formatter {formatter.Formatter} -- Formatter implementation
        filepath {str} -- path to a text file to load
    """

    def __init__(self, formatter, filepath: str):
        self._nlp = spacy.load('en')
        self._formatter = formatter

        with open(filepath, 'r') as f:
            lines = f.readlines()
            lines = [self._formatter.format(line) for line in lines]

        self._sentences = flatten([self._tokenise(line) for line in lines])

    def _tokenise(self, line: str) -> List[spacy.tokens.Span]:
        """Use the Spacy tokeniser to split a
        string into Spacy Span objects.

        Arguments:
            text {str} -- a string

        Returns:
            {List[spacy.tokens.Span]} -- list of Spacy tokenised sentences
        """

        doc = self._nlp(line)
        return doc.sents

    def __iter__(self):
        for sentence in self._sentences:
            yield sentence

    @property
    def sentences(self):
        return self._sentences
