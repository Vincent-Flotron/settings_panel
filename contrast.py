#! /bin/python3

# contrast.py
# -------------

import subprocess
import re
from   setting         import Setting
from   scale           import Scale
from   screen_settings import ScreenSettings
import gamma_formula as gf


class Contrast(Setting, Scale):
  def __init__(self, screen_name, min_value=0.0, max_value=100.0, limit_min_contrast=30.0, limit_max_contrast=100.0, scaled_min_value=0.2, scaled_max_value=1.5):
    super().__init__(min_value, max_value, limit_min_contrast, limit_max_contrast, "%", scaled_min_value, scaled_max_value)
    self.screen_name = screen_name

  def get_current_value(self):
    try:
      # Construct the xrandr command with screen_name
      command = (
        r"xrandr --verbose | grep -Poz '"
        + re.escape(self.screen_name)
        + r"(?:.*\r?\n){1,10}.*Gamma: *?(\d+\.?\d*)'"
      )
      # Execute the command and capture the output
      output = subprocess.check_output(
        command,
        shell   = True,
        text    = True,
        timeout = 5
      )
      # Extract the contrast value using regex
      contrast_match = re.search(r"Gamma: *?(\d+\.?\d*)", output)
      if contrast_match:
        self.set_normalized_value(float(contrast_match.group(1)))
        return self.get_val()
      else:
        print(f"Contrast value not found in xrandr output: {output}")
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
    ScreenSettings.set_gamma(gf.reverse(self.get_norm_val()))
    try:
      # Construct the xrandr command to set the contrast
      # command = f"xrandr --output {self.screen_name} --gamma {gf.reverse(self.get_norm_val())}:{gf.reverse(self.get_norm_val())}:{gf.reverse(self.get_norm_val())}"
      command = ScreenSettings.get_command()
      print(command)
      # Execute the command
      subprocess.run(
        command,
        shell   = True,
        timeout = 5,
        check   = True
      )
    except subprocess.CalledProcessError as e:
      print(f"Failed to run xrandr command: {e}")
    except subprocess.TimeoutExpired as e:
      print(f"xrandr command timed out: {e}")
    except Exception as e:
      print(f"Unexpected error occurred: {e}")
