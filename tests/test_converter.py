import pytest

from .. import converter
from measurement.measures import Distance


convert = converter.Converter(Distance())


def test_convert():
    conversion_mi = convert.convert([('1', 'mile')])
    assert conversion_mi == [('1609.34', 'm')]
    conversion_ft = convert.convert([('1', 'foot')])
    assert conversion_ft == [('0.3', 'm')]
    no_conversion = convert.convert([('1', 'm')])
    assert no_conversion == [('1.0', 'm')]
