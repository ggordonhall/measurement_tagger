"""Helper functions"""

from functools import reduce
from itertools import chain
from importlib import import_module

from typing import List, Any, Callable

from nltk.corpus import wordnet as wn


def map_funcs(obj: str, func_list: List[Callable]) -> str:
    """Apply series of functions to string"""
    return reduce(lambda o, func: func(o), func_list, obj)


def lower(lst: List[str]) -> List[str]:
    """Lowercase a list of strings"""
    return [s.lower() for s in lst]


def flatten(list_of_lists: List[List[Any]]) -> List[Any]:
    """Flatten a list of lists"""
    return list(chain.from_iterable(list_of_lists))


def strip_list(lst: List[str]) -> List[Any]:
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
    synset = wn.synset(synset_name)
    hypos = list(synset.closure(lambda s: s.hyponyms()))
    return set(flatten([synset.lemma_names() for synset in hypos]))
