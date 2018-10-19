"""Sentence iterator"""

import spacy
from tqdm import tqdm
from toolz import partition_all
from joblib import Parallel, delayed

from modules.utils import flatten


NLP = spacy.load('en', disable=['tagger', 'ner'])


class AbstractLoader:
    """Base class to load and tokenise sentences from a dataset.

    Arguments:
        formatter {formatter.Formatter} -- Formatter implementation
        filepath {str} -- path to a text file to load
    """

    def __init__(self, formatter, filepath):
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
        raise NotImplementedError

    def __iter__(self):
        for sentence in self._tokenise():
            yield sentence


class SentenceLoader(AbstractLoader):
    """Load and tokenise sentences with the Spacy tokeniser.

    Arguments:
        formatter {formatter.Formatter} -- Formatter implementation
        filepath {str} -- path to a text file to load
    """

    def __init__(self, formatter, filepath):
        super().__init__(formatter, filepath)

    def _tokenise(self):
        """Use the Spacy tokeniser to split
        lines into lists of Spacy Span objects.

        Yields:
            {List[spacy.tokens.Span]} --
                a list of Spacy tokenised sentences
        """

        lines = self._line_iter()
        for sent in tqdm(NLP.pipe(lines)):
            yield [span for span in sent]


class ParallelLoader(AbstractLoader):
    """Load and tokenise sentences in parallel with joblib and
    the Spacy tokeniser.

    Arguments:
        formatter {formatter.Formatter} -- Formatter implementation
        filepath {str} -- path to a text file to load
        batch_size {int} -- size of each job (default 1000)
        n_jobs {int} -- number of jobs (default 3)
    """

    def __init__(self, formatter, filepath, batch_size, n_jobs):
        super().__init__(formatter, filepath)
        self._batch_size = batch_size
        self._n_jobs = n_jobs

    def _tokenise(self):
        """Partition the dataset and run tokeniser in parallel."""

        partitions = partition_all(self._batch_size, self._line_iter())
        executor = Parallel(n_jobs=self._n_jobs)
        tasks = (delayed(subprocess)(NLP, part)
                 for part in partitions)
        return flatten(executor(tasks))


def subprocess(nlp, part):
    """Run the nlp pipeline on a subset of the dataset.

    Arguments:
        nlp {spacy.Pipe} -- a Spacy pipeline
        part {} -- a batch of the dataset
    """

    tokenised_sents = []
    for sent in nlp.pipe(part):
        tokenised_sents.append([span for span in sent])
    return tokenised_sents
