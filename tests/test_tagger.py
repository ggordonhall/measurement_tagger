import pytest
import spacy

from ..modules import tagger
from ..modules.utils import hyponyms
from ..modules.utils import Measurement


def test_hyponyms():
    assert 'cab' in hyponyms('car.n.01')
    with pytest.raises(ValueError):
        hyponyms('fgdfg')


tagger = tagger.Tagger(hyponyms('linear_unit.n.01'), 2, {})


def test_distance_tags():
    assert 'inch' in tagger._tags
    assert 'mile' in tagger._tags
    assert 'cubic meter' not in tagger._tags
    assert 'joule' not in tagger._tags
