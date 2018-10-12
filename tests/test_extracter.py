import pytest

from measurement.measures import Distance

from .. import extracter, tagger, formatter, converter


path = "test.txt"

tagger = tagger.DistanceTagger()
formatter = formatter.DistanceFormatter()
distance_container = Distance()
converter = converter.Converter(distance_container)

extracter_obj = extracter.Extracter(path, tagger, formatter, converter)


def test_extracter():
    extracter_obj.extract()
    pred_extracted = [("8046.72", "m"), ("1.83", "m"),
                      ("0.18", "m"), ("1.83", "m"), ("0.25", "m"),
                      ("4023.36", "m"), ("10972.8", "m")]
    assert extracter_obj._extracted == pred_extracted
