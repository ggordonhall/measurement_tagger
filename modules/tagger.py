"""Tagging class"""

from .utils import ints
from .utils import join
from .utils import overlapping
from .utils import Measurement


class Tagger:
    """Use the WordNet graph to extract measurements.

    Arguments:
        tags: {Set[str]} -- lemma tags to match
        max_gram: {int} -- maximum n-gram unit to match
        right_mod_tokens: {Dict[str, str]} --
            tokens mapped to their corresponding right modifier
    """

    def __init__(self, tags, max_gram, right_mod_tokens):
        self._tags = tags
        self._max_gram = max_gram
        self._right_mod_tokens = right_mod_tokens
        self._dep_modifiers = frozenset(['nummod', 'quantmod'])

    def tag(self, sentence):
        """Extract measurements from Spacy tokenised sentence.

        Arguments:
            sentence {List[spacy.tokens.Span]} -- a tokenised sentence

        Returns:
            {Optional[List[Union[Measurement, Tuple[Measurement]]]]} --
                a list of measurements or ``None``
        """

        measurements = []
        # iterate over sentence in decreasing n-grams
        for n in reversed(ints(1, self._max_gram)):
            for idx, n_gram in enumerate(overlapping(sentence, n)):
                # check if subset is a valid measurement
                subset = join([tok.lemma_ for tok in n_gram])
                if subset in self._tags:
                    # find numerical modifier on last token in subset
                    measure = self._measurements(n_gram[-1], subset)
                    if measure:
                        measurements.append(measure)
                        # delete subset so it is ignored by
                        # subsequent n-gram iterations
                        del sentence[idx: min(idx + n, len(sentence) - 1)]

        return measurements if measurements else None

    def _measurements(self, token, unit):
        """Given a token, get its left and right modifiers and
        construct a ``Measurement`` class. Tokens with left and right
        modifiers are returned as a tuple of ``Measurement``.

        Right modifiers are only supported for uni-gram units of
        measurement.

        Arguments:
            token {spacy.tokens.Token} -- a measurement Token
            unit {str} -- string representation of the measurement

        Returns:
            {Optional[Union[Measurement, Tuple[Measurement]]]} --
                measurement or None
        """

        left_mod = self._find_mod('l', token)
        if left_mod:
            l_measure = Measurement(left_mod, unit)
        # check if token could have numerical modifier to its right
        if token.lemma_ in self._right_mod_tokens.keys():
            right_mod = self._find_mod('r', token)
            if right_mod:
                r_unit = self._right_mod_tokens[token.lemma_]
                r_measure = Measurement(right_mod, r_unit)
                return (l_measure, r_measure)

        return l_measure

    def _find_mod(self, direction, token):
        """Given a token, search the dependency tree towards 'direction'
        for its numerical modifier.

        Arguments:
            token {spacy.tokens.Token} -- a measurement Token
            direction {Union['l', 'r']} --
                the direction to search the tree (left, right)

        Returns:
            {Optional[str]} -- the modifier's lemma
        """

        children = token.lefts if direction == 'l' else token.rights
        for adj_tok in children:
            if adj_tok.dep_ in self._dep_modifiers:
                return adj_tok.lemma_
        return None

    @property
    def tags(self):
        return self._tags

    @property
    def dependency_modifiers(self):
        return self._dep_modifiers
