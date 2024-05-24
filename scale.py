#! /bin/python3

# scale.py
# --------

from abc import ABC
from mesure import Mesure

class Scale(ABC):
    def __init__(self, min_value: float, max_value: float, limit_min_value: float, limit_max_value: float, unit: str, scaled_min_value: float=0, scaled_max_value: float=1):
        """
        Initializes the Scale object.

        :param min_value: Minimum scale value
        :param max_value: Maximum scale value
        :param limit_min_value: Minimum limit value
        :param limit_max_value: Maximum limit value
        :param unit: Unit of measurement
        """
        self.min = min_value
        self.max = max_value
        self.limit_min_value = limit_min_value
        self.limit_max_value = limit_max_value
        k = (min_value - max_value) / (scaled_min_value - scaled_max_value)
        offset = min_value - scaled_min_value * k
        self._mesure = Mesure(max_value, offset, k, unit)

    def get_min_value(self) -> float:
        """Returns the minimum value."""
        return self.min

    def get_max_value(self) -> float:
        """Returns the maximum value."""
        return self.max
    
    def get_limit_min_value(self) -> float:
        """Returns the minimum limit value."""
        return self.limit_min_value

    def get_limit_max_value(self) -> float:
        """Returns the maximum limit value."""
        return self.limit_max_value

    def set_normalized_value(self, value: float) -> None:
        """Sets the normalized value."""
        self._mesure.set_norm_val(value)

    def get_norm_val(self):
        """Gets the normalized value."""
        return self._mesure.get_norm_val()

    def get_val(self):
        """Gets the actual value from the normalized value."""
        return self._mesure.get_val()

    def set_val(self, value: float) -> None:
        """Sets the actual value, converting it to a normalized value."""
        self._mesure.set_val(value)

    def pretty_print(self):
        """Returns a formatted string of the actual value with its unit."""
        return self._mesure.pretty_print()
