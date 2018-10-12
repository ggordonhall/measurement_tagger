from functools import reduce
from itertools import chain

from typing import List, Any, Callable


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
