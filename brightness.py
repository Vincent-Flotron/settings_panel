#! /bin/python3

# brightness.py
# -------------

import subprocess
import re
from   setting         import Setting
from   scale           import Scale
from   screen_settings import ScreenSettings
from   observer        import Subject


class Brightness( Setting, Scale, Subject ):
  def __init__( self,
                screen_name,
                min_value            =   0.0,
                max_value            = 100.0,
                limit_min_brightness =  30.0,
                limit_max_brightness = 100.0,
                min_scaled_value     =   0.0,
                max_scaled_value     =   1.0,
                default_value        = 100.0,
                observer             = None):
    super().__init__(
      min_value,
      max_value,
      limit_min_brightness,
      limit_max_brightness,
      "%",
      min_scaled_value,
      max_scaled_value,
      default_value
    )
    Subject.__init__(self)
    self.screen_name      = screen_name
    # Prepare brightness regex
    self.brightness_regex = re.compile( r"Brightness: *?(\d\.?\d*)" )
    # For preparing cmd line to modify display
    super().attach(observer)


  def get_current_value( self ):
    try:
      # Construct the xrandr command with screen_name
      command = (
        r"xrandr --verbose | grep -Poz '"
        + re.escape( self.screen_name )
        + r"(?:.*\r?\n){1,10}.*Brightness: *?(\d\.?\d*)'"
      )
      # Execute the command and capture the output
      output = subprocess.check_output(
        command,
        shell   = True,
        text    = True,
        timeout = 5
      )
      # Extract the brightness value using regex
      brightness_match = self.brightness_regex.search( output )
      print(f"++++first brightness: {output}")
      if brightness_match:
        self.set_normalized_value( float( brightness_match.group(1) ) )
        super().notify( ( "gamma", self.get_norm_val() ) )
        return self.get_val()
      else:
        print( f"Brightness value not found in xrandr output: {output}" )
        return None
    except subprocess.CalledProcessError as e:
      print( f"Failed to run xrandr command: {e}" )
      return None
    except subprocess.TimeoutExpired as e:
      print( f"xrandr command timed out: {e}" )
      return None
    except Exception as e:
      print( f"Unexpected error occurred: {e}" )
      return None

  def set_value( self, value ):
    self.set_val( value )
    Subject.notify( self, ( "gamma", self.get_norm_val() ) )
    try:
      # Construct the xrandr command to set the brightness
      command = Subject.get_command(self)
      print( command )
      # Execute the command
      subprocess.run(
        command,
        shell   = True,
        timeout = 5,
        check   = True
      )
    except subprocess.CalledProcessError as e:
      print( f"Failed to run xrandr command: {e}" )
    except subprocess.TimeoutExpired as e:
      print( f"xrandr command timed out: {e}" )
    except Exception as e:
      print( f"Unexpected error occurred: {e}" )
