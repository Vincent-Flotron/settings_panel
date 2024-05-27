#! /bin/python3

# screen_settings.py
# ------------------


class ScreenSettings:
  _gamma       = None
  _brightness  = None
  _screen_name = None

  @staticmethod
  def set_gamma( value ):
    ScreenSettings._gamma = value

  @staticmethod
  def get_gamma():
    return ScreenSettings._gamma

  @staticmethod
  def set_brightness( value ):
    ScreenSettings._brightness = value

  @staticmethod
  def get_brightness():
    return ScreenSettings._brightness

  @staticmethod
  def set_screen_name( value ):
    ScreenSettings._screen_name = value

  @staticmethod
  def get_screen_name():
    return ScreenSettings._screen_name

  @staticmethod
  def get_command():
    return f"xrandr --output {ScreenSettings.get_screen_name()} --brightness {ScreenSettings.get_brightness()} --gamma {ScreenSettings.get_gamma()}:{ScreenSettings.get_gamma()}:{ScreenSettings.get_gamma()}"
          

