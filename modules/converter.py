"""Converter class"""

from .utils import two_round
from .utils import Measurement


class Converter:
    """Class to convert units to standard metric form."""

    def __init__(self, measurement_container, return_unconverted=False):
        """Set up measurement converter according to
        type of measurement container passed. Establish its
        standard unit to convert measurements to.

        Arguments:
            measurement_container {measurement.measures} --
                measurement container from the Python `measurement' library
            return_unconverted {bool} --
                return measurements which cannot be converted to standard form
                (default = False)
        """

        self._container = measurement_container
        self._standard_unit = self._container.STANDARD_UNIT
        self._return_unconverted = return_unconverted

    def convert(self, measurements):
        """Convert list of ``Measurement`` (value, unit) to standard form.

        Arguments:
            measurements {List[Measurement]]} -- ``Measurement`` list

        Yields:
            {Measurement} --
                ``Measurement`` class containing (value, unit) pairs
        """

        for measure in measurements:
            try:
                val = self._container.default_units(
                    {measure.unit: measure.value})[0]
                yield Measurement(two_round(val), self._standard_unit)
            except (ValueError, AttributeError):
                if self._return_unconverted:
                    yield measure
                else:
                    pass
