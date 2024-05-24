#! /bin/python3

# brightness.py
# -------------

import subprocess
import re
from   setting    import Setting
from   scale      import Scale


class Brightness(Setting, Scale):
  def __init__(self, screen_name, min_value=0.0, max_value=100.0, limit_min_brightness=30.0, limit_max_brightness=100.0):
    super().__init__(min_value, max_value, limit_min_brightness, limit_max_brightness, "%")
    self.screen_name = screen_name

  def get_current_value(self):
    try:
      # Construct the xrandr command with screen_name
      command = (
        r"xrandr --verbose | grep -Poz '"
        + re.escape(self.screen_name)
        + r"(?:.*\r?\n){1,10}.*Brightness: *?(\d\.?\d*)'"
      )
      # Execute the command and capture the output
      output = subprocess.check_output(
        command,
        shell=True,
        text=True,
        timeout=5
      )
      # Extract the brightness value using regex
      brightness_match = re.search(r"Brightness: *?(\d\.?\d*)", output)
      if brightness_match:
        self.set_normalized_value(float(brightness_match.group(1)))
        return self.get_val()
      else:
        print(f"Brightness value not found in xrandr output: {output}")
        return None
    except subprocess.CalledProcessError as e:
      print(f"Failed to run xrandr command: {e}")
      return None
    except subprocess.TimeoutExpired as e:
      print(f"xrandr command timed out: {e}")
      return None
    except Exception as e:
      print(f"Unexpected error occurred: {e}")
      return None

  def set_value(self, value):
    self.set_val(value)
    try:
      # Construct the xrandr command to set the brightness
      command = f"xrandr --output {self.screen_name} --brightness {self.get_norm_val()}"
      print(f"xrandr --output {self.screen_name} --brightness {self.get_norm_val()}")
      # Execute the command
      subprocess.run(
        command,
        shell=True,
        timeout=5,
        check=True
      )
    except subprocess.CalledProcessError as e:
      print(f"Failed to run xrandr command: {e}")
    except subprocess.TimeoutExpired as e:
      print(f"xrandr command timed out: {e}")
    except Exception as e:
      print(f"Unexpected error occurred: {e}")
