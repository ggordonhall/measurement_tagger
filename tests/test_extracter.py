import pytest

from measurement.measures import Distance

from ..modules import extractor, tagger, formatter, converter


path = "test.txt"
tags = ["mile", "inch", "foot", "fathom"]
right_mod = {"foot": "inch"}

tagger = tagger.Tagger(tags, right_mod)
formatter = formatter.DistanceFormatter()
distance_container = Distance()
converter = converter.Converter(distance_container)

extracter_obj = extractor.Extractor(path, tagger, formatter, converter)


def test_extracter():
    pred_extracted = set([("8046.72", "m"), ("1.83", "m"),
                          ("0.18", "m"), ("1.83", "m"), ("0.25", "m"),
                          ("4023.36", "m"), ("10972.8", "m")])
    assert set(extracter_obj.extract()) == pred_extracted
