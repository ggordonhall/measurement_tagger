"""Converter class"""

from modules.utils import two_round


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
        """Convert list of measurements (value, unit) to standard form.

        Arguments:
            measurements {List[Tuple[str, str]]} -- (value, unit) list

        Yields:
            {Tuple[str, str]} -- (value, unit) pairs
        """

        for measure in measurements:
            value, unit = measure
            try:
                value = self._container.default_units({unit: value})[0]
                conv_measure = (two_round(value), self._standard_unit)
                yield conv_measure
            except (ValueError, AttributeError):
                if self._return_unconverted:
                    yield measure
                else:
                    pass
