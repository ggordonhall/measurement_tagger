import pytest

from measurement.measures import Distance

from ..modules import extractor
from ..modules import tagger
from ..modules import formatter
from ..modules import converter
from ..modules.utils import Measurement


path = "tests/test.txt"
tags = ["mile", "inch", "foot", "fathom"]
max_gram = 2
right_mod = {"foot": "inch"}

tagger = tagger.Tagger(tags, max_gram, right_mod)
formatter = formatter.DistanceFormatter()
distance_container = Distance()
converter = converter.Converter(distance_container)

extractor_obj = extractor.Extractor(path, tagger, formatter, converter)


def test_extractor():
    pred_extracted = set([Measurement("8046.72", "m"), Measurement("2.01", "m"),
                          Measurement("2.08", "m")])
    assert set(extractor_obj.extract()) == pred_extracted
