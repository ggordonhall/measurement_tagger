"""Extractor pipeline"""

import os
from modules.loader import SentenceLoader
from modules.loader import ParallelLoader


class Extractor:
    """Measurement tagging pipeline class.

    Raises:
        FileNotFoundError -- when text file is not found

    Arguements:
        path {str} -- path to text file to extract
        tagger {Tagger} -- measurement tagging class
        formatter {Formatter} -- text formatting class
        converter {Converter} -- number conversion class

        parallel_opts {Tuple[int, int]} --
            options for parallel processing, (batch_size, n_jobs) pair.
            If None, loader is not run in parallel (default = None)
    """

    def __init__(self, path, tagger, formatter, converter, parallel_opts=None):
        if not os.path.exists(path):
            raise FileNotFoundError("Invalid filepath! {}".format(path))

        self._tagger = tagger
        self._converter = converter

        if parallel_opts:
            batch_size, n_jobs = parallel_opts
            self._sentences = ParallelLoader(
                formatter, path, batch_size, n_jobs)
        else:
            self._sentences = SentenceLoader(formatter, path)

    def extract(self):
        """Extract measurements from each sentence text file.

        Yields:
            {Tuple[str, str]} -- (value, unit) pairs
        """

        for sent in self._sentences:
            measures = self._tagger.tag(sent)
            if measures:
                for measure in self._converter.convert(measures):
                    yield measure
