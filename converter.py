from typing import List, Tuple

from utils import two_round


class Converter:
    """Class to convert units to standard metric form."""

    def __init__(self, measurement_container):
        """Set up measurement converter according to
        type of measurement container passed. Establish its
        standard unit to convert measurements to.

        Arguments:
            measurement_container {measurement.measures} --
                                measurement container from the Python
                                `measurement' library
        """

        self._container = measurement_container
        self._standard_unit = self._container.STANDARD_UNIT

    def convert(self, measurements: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """Convert list of measurements (value, unit) to standard form.

        Arguments:
            measurements {List[Tuple[str, str]]} -- (value, unit) list

        Returns:
            {List[Tuple[str, str]]} -- standard (value, unit) list
        """

        converted = []
        for measure in measurements:
            value, unit = measure
            try:
                value = self._container.default_units({unit: value})[0]
                conv_measure = (two_round(value), self._standard_unit)
                converted.append(conv_measure)
            except ValueError:
                converted.append(measure)

        return converted
