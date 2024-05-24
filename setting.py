#! /bin/python3

# setting.py
# ----------

from abc import ABC, abstractmethod

class Setting(ABC):
    """
    Abstract base class for settings.
    Defines the interface for getting and setting values.
    """

    @abstractmethod
    def get_current_value(self):
        """
        Retrieves the current value of the setting.
        :return: The current value.
        """
        pass

    @abstractmethod
    def set_value(self, value):
        """
        Sets the value of the setting.
        :param value: The value to set.
        """
        pass
