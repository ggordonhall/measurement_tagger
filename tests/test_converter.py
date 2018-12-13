import pytest

from measurement.measures import Distance
from measurement.measures import Mass

from ..modules.converter import Converter
from ..modules.utils import Measurement

dist_convert = Converter(Distance(), return_unconverted=True)


def test_convert_distance():
    conversion_mi = next(dist_convert.convert([Measurement('1', 'mile')]))
    assert conversion_mi == Measurement('1609.34', 'm')
    conversion_ft = next(dist_convert.convert([Measurement('1', 'foot')]))
    assert conversion_ft == Measurement('0.3', 'm')
    no_conversion = next(dist_convert.convert([Measurement('1', 'm')]))
    assert no_conversion == Measurement('1.0', 'm')
    conversion_compound = list(dist_convert.convert(
        [Measurement('two', 'foot'), Measurement('five', 'inch')]))
    assert conversion_compound == [Measurement(
        'two', 'foot'), Measurement('five', 'inch')]


mass_convert = Converter(Mass())


def test_convert_mass():
    conversion_kg = next(mass_convert.convert([Measurement('5', 'kg')]))
    assert conversion_kg == Measurement('5000.0', 'g')
