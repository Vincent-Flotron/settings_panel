# sound_output.py
# ---------------

from setting import Setting
import subprocess

class SoundOutput(Setting):
    def __init__(self):
        self.output_options = ["Speakers", "HDMI", "Bluetooth"]
        self.current_output = self.get_current_value()

    def get_current_value(self):
        try:
            output = subprocess.check_output("echo HDMI", shell=True, text=True).strip()
            if output in self.output_options:
                return output
            else:
                return "Speakers"  # Default value if output is unexpected
        except subprocess.CalledProcessError as e:
            print(f"Failed to get current sound output: {e}")
            return "Speakers"  # Default value on error

    def set_value(self, value):
        if value in self.output_options:
            self.current_output = value
            try:
                subprocess.run(f"echo {value}", shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to set sound output: {e}")
