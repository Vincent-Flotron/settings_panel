#! /bin/python3

# main.py
# -------

import configparser
from   brightness      import Brightness
from   sound_output    import SoundOutput
from   view            import View
from   contrast        import Contrast
from   screen_settings import ScreenSettings

# Load configuration from file
config = configparser.ConfigParser()
config.read( "config.ini" )

def get_config_option( section,
                       option,
                       default   = None,
                       type_func = str   ):
  try:
    return type_func( config.get( section, option ) )
  except ( configparser.NoSectionError, configparser.NoOptionError, ValueError ) as e:
    print( f"Error reading config [{section}] {option}: {e}" )
    return default

# Prepare for brightness and contrast settings
screen_settings = ScreenSettings()
screen_settings.set_screen_name( get_config_option( "contrast", "screen_name" ) )

# Create an instance of the Brightness class
brightness = Brightness(
  get_config_option( "brightness", "screen_name"                        ),
  get_config_option( "brightness", "min_brightness",         0.0, float ),
  get_config_option( "brightness", "max_brightness",       100.0, float ),
  get_config_option( "brightness", "limit_min_brightness",  30.0, float ),
  get_config_option( "brightness", "limit_max_brightness", 100.0, float ),
  get_config_option( "brightness", "min_scaled_brightness",  0.0, float ),
  get_config_option( "brightness", "max_scaled_brightness",  1.0, float ),
  get_config_option( "brightness", "default_brightness",    90.0, float ),
  screen_settings
)

# Create an instance of the Contrast class
contrast = Contrast(
  get_config_option( "contrast", "screen_name"                      ),
  get_config_option( "contrast", "min_contrast",         0.0, float ),
  get_config_option( "contrast", "max_contrast",       100.0, float ),
  get_config_option( "contrast", "limit_min_contrast",  30.0, float ),
  get_config_option( "contrast", "limit_max_contrast", 100.0, float ),
  get_config_option( "contrast", "scaled_min_contrast",  0.2, float ),
  get_config_option( "contrast", "scaled_max_contrast",  1.5, float ),
  get_config_option( "contrast", "default_contrast",    90.0, float ),
  screen_settings
)

# Create an instance of the Sound Output class
sound_output = SoundOutput(
  get_config_option( 
    "sound",
    "choices",
    "Speakers," +
    "HDMI"
  ),
  get_config_option( 
    "sound", 
    "cards",
    "alsa_card.pci-0000_00_1b.0," +
    "alsa_card.pci-0000_00_1b.0"
  ),
  get_config_option( 
    "sound", 
    "card_outputs",
    "alsa_output.pci-0000_00_1b.0," +
    "alsa_output.pci-0000_00_1b.0"
  ),
  get_config_option( 
    "sound",
    "configurations",
    "output:analog-stereo+input:analog-stereo," +
    "output:iec958-stereo+input:analog-stereo"
  ),
  get_config_option( 
    "sound",
    "outputs",
    "analog-stereo," +
    "iec958-stereo"
  ),
  get_config_option( 
    "sound",
    "ports",
    "analog-output-speaker," +
    "iec958-stereo-output"
  )
)

# Get actual values
print("============================1")
brightness.get_current_value()
contrast.get_current_value()
print("============================2")
# Set default value of brightness
brightness.set_value(
  get_config_option(
    "brightness",
    "default_brightness",
    100.0,
    float 
  )
)

print("============================3")
# Set default value of contrast
contrast.set_value(
  get_config_option( 
    "contrast",
    "default_contrast",
    100.0,
    float
  )
)

print("============================4")
# Create the GUI view for brightness and sound output control
view = View(
  brightness,
  sound_output,
  contrast,
  get_config_option( 
    "theme",
    "themes",
    "arc,clam,alt,default,classic"
  ),
  get_config_option(
    "theme",
    "default_theme",
    "clam"
  )
)

# Start the main event loop
view.run()
