import pytest

from .. import tagger
from ..tagger import hyponyms


tagger = tagger.DistanceTagger()


def test_hyponyms():
    assert 'cab' in hyponyms('car.n.01')
    with pytest.raises(ValueError):
        hyponyms('fgdfg')


def test_distance_tags():
    assert 'inch' in tagger._tags
    assert 'mile' in tagger._tags
    assert 'cubic_meter' not in tagger._tags
    assert 'joule' not in tagger._tags
