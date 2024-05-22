# reglages.py
# -----------

import configparser
from brightness import Brightness
from view import View

# Load configuration from file
config = configparser.ConfigParser()
config.read("config.ini")

def get_config_option(section, option, default=None, type_func=str):
    try:
        return type_func(config.get(section, option))
    except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
        print(f"Error reading config [{section}] {option}: {e}")
        return default

# Create an instance of the Brightness class
brightness = Brightness(
    get_config_option("brightness", "screen_name"),
    get_config_option("brightness", "min_brightness", 0.0, float),
    get_config_option("brightness", "max_brightness", 100.0, float),
    get_config_option("brightness", "limit_min_brightness", 30.0, float),
    get_config_option("brightness", "limit_max_brightness", 100.0, float)
)

# Create the GUI view for brightness and sound output control
view = View(brightness)

# Start the main event loop
view.run()
