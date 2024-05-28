from   observer      import Observer
import gamma_formula as gf

class ScreenSettings( Observer ):
  def __init__( self ):
    self._gamma       = None
    self._brightness  = None
    self._screen_name = None

  def update(self, subject):
    attr, value = subject
    if  ( attr == "brightness" ):
      self.set_brightness( value )
    elif( attr == "gamma" ):
      self.set_gamma( gf.reverse( value ) )
    # TODO

  def set_gamma( self, value ):
    self._gamma = value

  def get_gamma( self ):
    return self._gamma

  def set_brightness( self, value ):
    self._brightness = value

  def get_brightness( self ):
    return self._brightness

  def set_screen_name( self, value ):
    self._screen_name = value

  def get_screen_name( self ):
    return self._screen_name

  def get_command( self ):
    if( self.get_brightness() == None ):
      raise Exception("Error in screen_settings.get_command(): method called before brightness set.")
    if( self.get_gamma()      == None ):
      raise Exception("Error in screen_settings.get_command(): method called before Gamma set.")
    return f"xrandr --output {self.get_screen_name()} " + \
           f"--brightness {self.get_brightness()} "     + \
           f"--gamma {self.get_gamma()}:"               + \
           f"{self.get_gamma()}:"                       + \
           f"{self.get_gamma()}"
