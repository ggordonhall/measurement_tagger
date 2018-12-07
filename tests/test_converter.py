import pytest

from measurement.measures import Distance

from ..modules.converter import Converter
from ..modules.utils import Measurement

convert = Converter(Distance())


def test_convert():
    conversion_mi = next(convert.convert([Measurement('1', 'mile')]))
    assert conversion_mi == Measurement('1609.34', 'm')
    conversion_ft = next(convert.convert([Measurement('1', 'foot')]))
    assert conversion_ft == Measurement('0.3', 'm')
    no_conversion = next(convert.convert([Measurement('1', 'm')]))
    assert no_conversion == Measurement('1.0', 'm')
