#! /bin/python3

# screen_settings.py
# ------------------

import threading

class ScreenSettings:
    _gamma       = None
    _brightness  = None
    _screen_name = None
    _lock        = threading.Lock()

    @staticmethod
    def set_gamma(value):
        with ScreenSettings._lock:
            ScreenSettings._gamma = value

    @staticmethod
    def get_gamma():
        with ScreenSettings._lock:
            return ScreenSettings._gamma

    @staticmethod
    def set_brightness(value):
        with ScreenSettings._lock:
            ScreenSettings._brightness = value

    @staticmethod
    def get_brightness():
        with ScreenSettings._lock:
            return ScreenSettings._brightness

    @staticmethod
    def set_screen_name(value):
        with ScreenSettings._lock:
            ScreenSettings._screen_name = value

    @staticmethod
    def get_screen_name():
        with ScreenSettings._lock:
            return ScreenSettings._screen_name


