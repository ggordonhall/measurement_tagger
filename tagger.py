from typing import List, Set, Tuple, Union, Optional

import spacy
from nltk.corpus import wordnet as wn

from utils import flatten


DISTANCE_SYNSET = 'linear_unit.n.01'


class Tagger:
    """Base tagging class."""

    def tag(self, sentence: List[spacy.tokens.Span]):
        """Tags a Spacy tokenised sentence.

        Arguments:
            sentence {List[spacy.tokens.Span]} -- tokens to tag
        """
        raise NotImplementedError


class DistanceTagger(Tagger):
    """Use the WordNet graph to extract sentences
    containing distance measurements.

    Arguments:
        tags: {Set[str]} -- distance lemma tags to match
    """

    def __init__(self):
        super(DistanceTagger, self).__init__()
        self._tags = hyponyms(DISTANCE_SYNSET)
        self._dep_modifiers = frozenset(['nummod', 'quantmod'])
        # tokens which might have a modifier to their right
        self._right_mod_tokens = {'foot': 'inch'}

    def tag(self, sentence: List[spacy.tokens.Span]) -> Optional[
            List[Tuple[str, str]]]:
        """Takes a Spacy tokenised sentence and extracts
        distance measurements.

        Arguments:
            sentence {List[spacy.tokens.Span]} - - the tokenised sentence to
                                                    extract measurements from
        Returns:
            {Optional[List[Tuple[str, str]]]} - -
                a list of tuples of(numerical modifiers and tokens) or None
        """

        measurements = []
        for token in sentence:
            if token.lemma_ in self._tags:
                modifier = self._measurements(token)
                if modifier:
                    measurements.extend(modifier)
        return measurements if measurements else None

    def _measurements(self, token: spacy.tokens.Token) -> Optional[
            List[Tuple[str, str]]]:
        """Given a token, gets its modifiers to its left and right.

        Arguments:
            token {spacy.tokens.Token} - - a measurement Token

        Returns:
            {Optional[List[[Tuple[str, str]]} - -
                a list of(numerical modifier and the token) or None
        """

        modifiers = []
        left_mod = self._find_mod('l', token)
        if left_mod:
            modifiers.append((left_mod, token.lemma_))
        # check if token could have numerical modifier to its right
        if token.lemma_ in self._right_mod_tokens.keys():
            right_mod = self._find_mod('r', token)
            if right_mod:
                modifiers.append(
                    (right_mod, self._right_mod_tokens[token.lemma_]))
        return modifiers

    def _find_mod(self, direction: Union['l', 'r'],
                  token: spacy.tokens.Token) -> Optional[str]:
        """Given a token, search the dependency tree towards 'direction'
        for its numerical modifier.

        Arguments:
            token {spacy.tokens.Token} - - a measurement Token
            direction {Union['l', 'r']} - - the direction to search the tree
                                            (left, right)

        Returns:
            {Optional[str]} - - the modifier's lemma
        """

        children = token.lefts if direction == 'l' else token.rights
        for adj_tok in children:
            if adj_tok.dep_ in self._dep_modifiers:
                return adj_tok.lemma_
        return None

    @property
    def distance_tags(self):
        return self._tags

    @property
    def dependency_modifiers(self):
        return self._dep_modifiers


def hyponyms(synset_name: str) -> Set[str]:
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
