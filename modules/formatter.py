"""Sentence formatter"""

import re
from modules.utils import flatten, map_funcs, strip_list


class Formatter:
    """Base class for formatting."""

    def __init__(self):
        self._replace_funcs = []

    def format(self, line):
        """Format line of text for tagging.
        Apply specialised replacement functions.

        Arguments:
            line {str} -- unmodified line

        Returns:
            line {str} -- formatted line
        """
        tokens = strip_list(line.lower().split())
        split_toks = flatten([split_numerals(tok) for tok in tokens])
        replace_toks = [map_funcs(tok, self._replace_funcs)
                        for tok in split_toks]
        return ' '.join(replace_toks)


class DistanceFormatter(Formatter):
    """Format text for distance tagging."""

    def __init__(self):
        super(DistanceFormatter, self).__init__()
        self._replace_funcs = [remove_commas,
                               replace_feet_inches,
                               replace_ft]


class MassFormatter(Formatter):
    """Format text for mass tagging."""

    def __init__(self):
        super(MassFormatter, self).__init__()
        self._replace_funcs = [remove_commas]


class TimeFormatter(Formatter):
    """Format text for time tagging."""

    def __init__(self):
        super(TimeFormatter, self).__init__()
        self._replace_funcs = [remove_commas,
                               remove_quarter,
                               remove_moon]


class VolumeFormatter(Formatter):
    """Format text for volume tagging."""

    def __init__(self):
        super(VolumeFormatter, self).__init__()
        self._replace_funcs = [remove_commas,
                               remove_quarter]


class EnergyFormatter(Formatter):
    """Format text for energy tagging."""

    def __init__(self):
        super(EnergyFormatter, self).__init__()
        self._replace_funcs = [remove_commas]


### GENERAL REPLACEMENT FUNCTIONS ###

def split_numerals(token):
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


def remove_commas(token):
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


### DISTANCE REPLACEMENT FUNCTIONS ###

def replace_feet_inches(token):
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


def replace_ft(token):
    """Normalise ft tokens.
    e.g. "ft" -> "foot"

    Arguments:
        token {str} -- a string to replace

    Returns:
        {str} -- a replaced string
    """
    return 'foot' if token == 'ft' else token


### TIME REPLACEMENT FUNCTIONS ###

def remove_moon(token):
    """Remove `moon`, an archaic unit
    of time which confuses the tagger.

    Arguments:
        token {str} -- a string to replace

    Returns:
        {str} -- a replaced string
    """

    moon = ["moon", "moons"]
    return "" if token in moon else token


### OTHER REPLACEMENT FUNCTIONS ###

def remove_quarter(token):
    """Remove `quarter`, a unit
    of volume or time which confuses the tagger.

    Arguments:
        token {str} -- a string to replace

    Returns:
        {str} -- a replaced string
    """

    pred_a = token in ["quarter", "quarters"]
    pred_b = "-quarter" in token
    return "" if pred_a or pred_b else token
