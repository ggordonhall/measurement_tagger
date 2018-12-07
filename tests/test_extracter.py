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

extracter_obj = extractor.Extractor(path, tagger, formatter, converter)


def test_extracter():
    pred_extracted = set([Measurement("8046.72", "m"), Measurement("1.83", "m"),
                          Measurement("0.18", "m"), Measurement(
                              "1.83", "m"), Measurement("0.25", "m"),
                          Measurement("4023.36", "m"), Measurement("10972.8", "m")])
    assert set(extracter_obj.extract()) == pred_extracted
