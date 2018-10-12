import re
from typing import List

from utils import flatten, map_funcs, strip_list


class Formatter:
    """Base class for formatting."""

    def format(self, line: str) -> str:
        """Format line of text for tagging.
        Apply specialised replacement functions.

        Arguments:
            line {str} -- unmodified line

        Returns:
            line {str} -- formatted line
        """
        raise NotImplementedError


class DistanceFormatter(Formatter):
    """Format text for distance tagging."""

    def __init__(self):
        super(DistanceFormatter, self).__init__()
        self._replace_funcs = [remove_commas,
                               replace_feet_inches,
                               replace_ft]

    def format(self, line: str) -> str:
        """Format line of text for distance tagging.
        Create tokens by separating alphanumic strings, then
        apply replacement functions.

        Arguments:
            line {str} -- unmodified line

        Returns:
            line {str} -- formatted line
        """
        tokens = strip_list(line.split())
        split_toks = flatten([split_numerals(tok) for tok in tokens])
        replace_toks = [map_funcs(tok, self._replace_funcs)
                        for tok in split_toks]
        return ' '.join(strip_list(replace_toks))


def split_numerals(token: str) -> List[str]:
    """Split conjoined alphanumeric strings.
    e.g. "aa1" -> ["aa", "1"]

    Arguments:
        token {str} -- a string to split

    Returns:
        {List[str]} -- a list of split strings
    """

    split_regex = r'^([0-9]+)([a-z]+)([0-9]+)?$'
    match = re.match(split_regex, token, re.I)
    return [g for g in match.groups() if g] if match else [token]


def replace_feet_inches(token: str) -> str:
    """Replace punctuations marks for feet and inches with words.
    e.g. 5'7" -> 5 foot 7 inch
         3' -> 3 foot

    Arguements:
        token {str} -- a string to replace

    Returns:
        {str} -- a replaced string
    """
    ft_in_regex = r'(?!$)(\(?[0-9]+\'){1}([0-9]+\x22?\)?)?'
    if re.match(ft_in_regex, token):
        token = token.replace("'", ' foot ')
        if u'\x22' in token:
            token = token.replace(u'\x22', ' inch')
        elif token[-1].isdigit():
            token += ' inch'
    return token


def replace_ft(token: str) -> str:
    """Normalise ft tokens.
    e.g. "ft" -> "foot"

    Arguments:
        token {str} -- a string to replace

    Returns:
        {str} -- a replaced string
    """
    return 'foot' if token == 'ft' else token


def remove_commas(token: str) -> str:
    """Remove commas in numbers.
    e.g. "5,000" -> "5000"

    Arguments:
        token {str} -- a string

    Returns:
        {str} -- string without commas if
               it is numerical
    """
    comma_regex = r'[()0-9,]+'
    if re.match(comma_regex, token):
        token = token.replace(',', '')
    return token
