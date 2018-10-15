from typing import List, Set, Dict, Tuple, Union, Optional

import spacy


class Tagger:
    """Use the WordNet graph to extract measurements.

    Arguments:
        tags: {Set[str]} -- lemma tags to match
        right_mod_tokens: {Dict[str, str]} --
            tokens mapped to their corresponding right modifier
    """

    def __init__(self, tags: Set[str], right_mod_tokens: Dict[str, str]):
        self._tags = tags
        self._right_mod_tokens = right_mod_tokens
        self._dep_modifiers = frozenset(['nummod', 'quantmod'])

    def tag(self, sentence: List[spacy.tokens.Span]) -> Optional[
            List[Tuple[str, str]]]:
        """Extract measurements from Spacy tokenised sentence.

        Arguments:
            sentence {List[spacy.tokens.Span]} - - a tokenised sentence

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
            direction {Union['l', 'r']} - -
                the direction to search the tree (left, right)

        Returns:
            {Optional[str]} - - the modifier's lemma
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
