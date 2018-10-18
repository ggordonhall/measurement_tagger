"""Extractor pipeline"""

import os
from loader import SentenceLoader


class Extractor:
    """Measurement tagging pipeline class.

    Raises:
        FileExistsError -- when text file is not found

    Arguements:
        path {str} -- path to text file to extract
        tagger {Tagger} -- measurement tagging class
        formatter {Formatter} -- text formatting class
        converter {Converter} -- number conversion class
    """

    def __init__(self, path, tagger, formatter, converter):
        if not os.path.exists(path):
            raise FileExistsError("Invalid filepath! {}".format(path))

        self._tagger = tagger
        self._converter = converter
        self._sentences = SentenceLoader(formatter, path)

        self._extracted = []

    def extract(self):
        """Extract measurements from each sentence text file."""

        for sent in self._sentences:
            measures = self._tagger.tag(sent)
            if measures:
                converted = self._converter.convert(measures)
                self._extracted.extend(converted)

    def __repr__(self):
        unpack = [' '.join(m) for m in self._extracted]
        return '\n'.join(unpack)
