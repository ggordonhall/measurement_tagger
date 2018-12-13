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
        """Convert list of measurements to standard form. If a
        measurement is a tuple, combine the units into a single
        value:
            (i.e. 3 foot 2 inch) -> 0.96 metres

        Arguments:
            measurements {List[Union[Measurement, Tuple[Measurement]]]} --
                list of measurements

        Yields:
            {Union[Measurement, Tuple[Measurement]]} --
                a converted measurement
        """

        for measure in measurements:
            try:
                if isinstance(measure, tuple):
                    val = sum(map(self._std, measure))
                else:
                    val = self._std(measure)
                yield Measurement(two_round(val), self._standard_unit)

            except (ValueError, AttributeError):
                if self._return_unconverted:
                    yield measure
                else:
                    pass

    def _std(self, measure):
        """Convert  ``Measurement`` to standard form.

        Arguments:
            measure {Measurement} -- a ``Measurement``

        Returns:
            {float} -- measurement value in standard form
        """

        return self._container.default_units({measure.unit: measure.value})[0]
