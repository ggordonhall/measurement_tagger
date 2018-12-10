"""Helper functions"""

from functools import reduce
from itertools import chain
from importlib import import_module
from collections.abc import Sequence

from dataclasses import dataclass

from typing import List, Any, Callable, Iterable, Iterator


@dataclass(frozen=True)
class Measurement:
    """Dataclass containing measurement value and unit"""
    value: str
    unit: str

    def __str__(self):
        return f"{self.value} {self.unit}"


def map_funcs(obj: str, func_list: List[Callable]) -> str:
    """Apply series of functions to string"""
    return reduce(lambda o, func: func(o), func_list, obj)


def lower(lst: List[str]) -> List[str]:
    """Lowercase a list of strings"""
    return [s.lower() for s in lst]


def join(iterable: Iterable, sep: str = " ") -> str:
    """Join an interable with sep"""
    return sep.join(map(str, iterable))


def ints(start: int, end: int) -> Iterator:
    """The integers from start to end, inclusive"""
    return range(start, end + 1)


def flatten(list_of_lists: List[List[Any]]) -> List[Any]:
    """Flatten a list of lists"""
    return list(chain.from_iterable(list_of_lists))


def overlapping(iterable: Iterable, n: int) -> Iterator:
    """Generate all (overlapping) n-element subsequences of iterable"""
    assert isinstance(iterable, Sequence)
    yield from (iterable[i: i + n] for i in range(len(iterable) + 1 - n))


def strip_list(lst: List[str]) -> List[str]:
    """Strip whitespace from list of strings"""
    return [l.strip() for l in lst if l is not None]


def two_round(num: float) -> str:
    """Return str of num rounded to 2 sig"""
    return str(round(num, 2))


def get_class(module: str, class_: str) -> Any:
    """Get instantiated class given name and module"""
    clazz = getattr(import_module(module), class_)
    return clazz()


def hyponyms(synset_name):
    """Given a WordNet synset name, return the lemmas of
    all its hyponyms in the WordNet semantic graph.

    Arguments:
        synset_name {str} -- a high-level synset

    Returns:
        {Set[str]} -- set of hyponyms
    """
    from nltk.corpus import wordnet as wn

    synset = wn.synset(synset_name)
    hypos = list(synset.closure(lambda s: s.hyponyms()))
    lemmas = flatten([synset.lemma_names() for synset in hypos])
    return {l.replace("_", " ") for l in lemmas}
