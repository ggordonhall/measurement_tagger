"""Sentence iterator"""

import spacy
from tqdm import tqdm


class SentenceLoader:
    """Load and tokenise sentences from a dataset.

    Arguments:
        formatter {formatter.Formatter} -- Formatter implementation
        filepath {str} -- path to a text file to load
    """

    def __init__(self, formatter, filepath):
        self._nlp = spacy.load('en', disable=['tagger', 'ner'])
        self._formatter = formatter
        self._filepath = filepath

    def _line_iter(self):
        """Read and format lines in the file.

        Yields:
            {str} -- a formatted line
        """

        with open(self._filepath, 'r') as f:
            for line in f:
                yield self._formatter.format(line)

    def _tokenise(self):
        """Use the Spacy tokeniser to split
        lines into lists of Spacy Span objects.

        Yields:
            {List[spacy.tokens.Span]} --
                a list of Spacy tokenised sentences
        """

        lines = self._line_iter()
        for sent in tqdm(self._nlp.pipe(lines)):
            yield [span for span in sent]

    def __iter__(self):
        for sentence in self._tokenise():
            yield sentence
