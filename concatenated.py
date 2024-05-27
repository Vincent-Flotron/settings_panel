#! /bin/python3

# contrast.py
# -------------

import subprocess
import re
from   setting         import Setting
from   scale           import Scale
from   screen_settings import ScreenSettings
import gamma_formula   as gf


class Contrast( Setting, Scale ):
  def __init__( self,
                screen_name,
                min_value          =   0.0,
                max_value          = 100.0,
                limit_min_contrast =  30.0,
                limit_max_contrast = 100.0,
                scaled_min_value   =   0.2,
                scaled_max_value   =   1.5,
                default_value      = 100.0 ):
    super().__init__(
      min_value,
      max_value,
      limit_min_contrast,
      limit_max_contrast,
      "%",
      scaled_min_value,
      scaled_max_value,
      default_value
    )
    self.screen_name    = screen_name
    self.set_value( default_value )
    
    self.contrast_regex = re.compile( r"Gamma: *?(\d+\.?\d*)" )

  def get_current_value( self ):
    try:
      # Construct the xrandr command with screen_name
      command = (
        r"xrandr --verbose | grep -Poz '"            +
        re.escape( self.screen_name )                +
        r"(?:.*\r?\n){1,10}.*Gamma: *?(\d+\.?\d*)'"
      )
      # Execute the command and capture the output
      output = subprocess.check_output(
        command,
        shell   = True,
        text    = True,
        timeout = 5
      )
      # Extract the contrast value using regex
      contrast_match = self.contrast_regex.search( output )
      if contrast_match:
        self.set_normalized_value( float( contrast_match.group(1) ) )
        return self.get_val()
      else:
        print( f"Contrast value not found in xrandr output: {output}" )
        return None
    except subprocess.CalledProcessError as e:
      print( f"Failed to run xrandr command: {e}")
      return None
    except subprocess.TimeoutExpired as e:
      print( f"xrandr command timed out: {e}" )
      return None
    except Exception as e:
      print( f"Unexpected error occurred: {e}" )
      return None

  def set_value( self, value ):
    self.set_val( value )
    ScreenSettings.set_gamma( gf.reverse( self.get_norm_val() ) )
    try:
      # Construct the xrandr command to set the contrast
      command = ScreenSettings.get_command()
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

#======================================================================#
#! /bin/python3

# sound_output.py
# ---------------

from   setting    import Setting
import subprocess
import re

class SoundOutput( Setting ):
  def __init__( self,
                choices,
                cards,
                card_outputs,
                configurations,
                outputs,
                ports          ):
    self.choices        = choices.split( ',' )
    self.cards          = cards.split( ',' )
    self.card_outputs   = card_outputs.split( ',' )
    self.configurations = configurations.split( ',' )
    self.outputs        = outputs.split( ',' )
    self.ports          = ports.split( ',' )
    
    # Initialize profile_regex
    self.profile_regex       = re.compile(
      r"Nom\s*:\s*" +
      re.escape( self.cards[0] ) +
      r".*\r?\n(?:\t.*\r?\n)*\tProfil actif\s*:\s*output:(.+?)[\+|$]"
    )
    
    # Initialize actual_config_regex
    self.actual_config_regex = re.compile(
      r"Nom\s*:\s*" + 
      re.escape( self.cards[0] ) + 
      r".*\r?\n(?:\t.*\r?\n)*\tProfil actif\s*:\s*(.+)"
    )
    
    # Get the current output value
    self.current_output = self.get_current_value()

  def get_current_value( self ):
    try:
      # Get the actual profile used
      pactl_list_cards    = subprocess.check_output(
        "pactl list cards",
        shell = True,
        text  = True
      ).strip()
      actual_profil_match = self.profile_regex.search( pactl_list_cards )
      actual_config_match = self.actual_config_regex.search( pactl_list_cards )

      if actual_profil_match:
        actual_profil = actual_profil_match.group(1).strip()
        print( f"Actual profile: {actual_profil}" )
      else:
        raise ValueError( "Failed to match actual profile." )

      if actual_config_match:
        actual_config = actual_config_match.group(1).strip()
        print( f"Actual config: {actual_config}" )
      else:
        raise ValueError( "Failed to match actual config." )

      # Get the actual port used
      pactl_list_sinks = subprocess.check_output(
        "pactl list sinks",
        shell = True,
        text  = True
      ).strip()
      port_regex = re.compile(
        r"Nom\s*:\s*" + re.escape( self.card_outputs[0] ) + 
        r"." + re.escape( actual_profil )                 + 
        r".*\r?\n(?:\t.*\r?\n)*\tPort actif\s*:\s*(.+)"
      )
      actual_port_match = port_regex.search( pactl_list_sinks )

      if actual_port_match:
        actual_port = actual_port_match.group(1).strip()
        print( f"Actual port: {actual_port}" )
      else:
        raise ValueError( "Failed to match actual port." )

      choice = self.find_choice_from( actual_config, actual_port )

      # Return the actual output (choice)
      return choice

    except subprocess.CalledProcessError as e:
      print( f"Failed to get current sound output: {e}" )
      return "Speakers"  # Default value on error
    except ValueError as e:
      print( e )
      return "Speakers"  # Default value on error

  def find_choice_from( self, config, port ):
    try:
      conf_ind = self.configurations.index( config )
    except ValueError:
      print( f"Config '{config}' not found in the configuration list." )
      return None
    try:
      port_ind = self.ports.index( port )
    except ValueError:
      print( f"Port '{port}' not found in the port list." )
      return None
    if conf_ind == port_ind:
      return self.choices[ port_ind ]
    else:
      print( 
        f"Configuration and port indices " +
        f"do not match: {conf_ind} != {port_ind}"
      )
      return None

  def find_choice_index( self, choice ):
    try:
      return self.choices.index( choice )
    except ValueError:
      print( f"Choice '{choice}' not found in the choice list." )
      return None

  def set_value( self, value ):
    print( f"Setting value: {value}, Choices: {self.choices}" )
    if value in self.choices:
      choice_index = self.find_choice_index( value )
      if choice_index is not None:
        cmd_set_profile =                          \
          f"pactl set-card-profile "             + \
          f"{self.cards[choice_index]} "         + \
          f"{self.configurations[choice_index]}"
        cmd_set_port    =                                                      \
          f"pactl set-sink-port "                                            + \
          f"{self.card_outputs[choice_index]}.{self.outputs[choice_index]} " + \
          f"{self.ports[choice_index]}"
        try:
          subprocess.run( cmd_set_profile, shell=True, check=True )
          subprocess.run( cmd_set_port,    shell=True, check=True )
          self.current_output = value
        except subprocess.CalledProcessError as e:
          print( f"Failed to set sound output: {e}" )
    else:
      print( f"Value '{value}' is not a valid choice." )

#======================================================================#
#! /bin/python3

# widget.py
# ---------

import tkinter as tk
from   tkinter import ttk

class Widget:
  def __init__( self,
                root,
                label_text,
                control_obj ):
    self.root        = root
    self.control_obj = control_obj
    
    # Label for the Widget
    self.label = ttk.Label( self.root, text=label_text )
    self.label.pack( pady=10 )
    
    # Display label for current value
    self.value_label = ttk.Label( self.root, text="" )
    self.value_label.pack( pady=10 )
    
  def update_value_label( self, value ):
    self.value_label.config( text=f"Current Value: {value}" )
    

class WidgetScale( Widget ):
  def __init__( self,
                root,
                label_text,
                control_obj ):
    super().__init__( root, label_text, control_obj )
    
    # Scale for the widget
    actual_value = control_obj.get_current_value()
    self.scale   = ttk.Scale(
      self.root,
      from_   = control_obj.get_limit_min_value(),
      to      = control_obj.get_limit_max_value(),
      orient  = "horizontal",
      value   = actual_value if   actual_value is not None 
                             else control_obj.get_norm_val(),
      command = self.on_scale_change
    )
    self.scale.pack( pady=20 )
    
    # Bind the scale event
    self.scale.bind( "<ButtonRelease-1>", self.on_scale_release )
    super().update_value_label( if actual_value != None: round(actual_value, 2) else: actual_value )

  def on_scale_event( self ):
    try:
      value = self.scale.get()
      if value != self.control_obj.get_val():
        self.control_obj.set_value( value )
        actual_value = self.control_obj.get_current_value()
        self.update_value_label( self.control_obj.pretty_print() )
    except Exception as e:
      print( f"Error adjusting scale: {e}" )
      super().update_value_label( "Error adjusting scale" )
      
  def on_scale_release( self, event ):
    self.on_scale_event()
    
  def on_scale_change( self, event ):
    self.on_scale_event()

class WidgetRadioButton( Widget ):
  def __init__( self,
                root,
                label_text,
                control_obj ):
    super().__init__( root, label_text, control_obj )

    # Radio for the widget
    self.radio_var = tk.StringVar( value=self.control_obj.get_current_value() )
    for option in self.control_obj.choices:
      rb = tk.ttk.Radiobutton(
        self.root,
        text     = option,
        variable = self.radio_var,
        value    = option,
        command  = self.on_radio_change
      )
      rb.pack( anchor=tk.W )
    
  def on_radio_change( self ):
    try:
      selected_output = self.radio_var.get()
      self.control_obj.set_value( selected_output )
    except Exception as e:
      print( f"Error changing radio button: {e}" )
    super().update_value_label( self.control_obj.get_current_value() )

  def on_scale_event( self ):
    try:
      value = self.scale.get()
      if value != self.control_obj.get_val():
        self.control_obj.set_value( value )
        actual_value = self.control_obj.get_current_value()
        self.update_value_label( self.control_obj.pretty_print() )
    except Exception as e:
      print( f"Error adjusting scale: {e}" )
      super().update_value_label( "Error adjusting scale" )
      
  def on_scale_release( self, event ):
    self.on_scale_event()
    
  def on_scale_change( self, event ):
    self.on_scale_event()
    
class WidgetBuilder:
  # Widget's types
  type_scale = "scale"
  type_radio = "radio"
  
  def make( root,
            label_text,
            control_obj,
            widget_type ):
    if ( widget_type == WidgetBuilder.type_scale ):
      return WidgetScale(
        root        = root,
        label_text  = label_text,
        control_obj = control_obj
      )
    elif ( widget_type == WidgetBuilder.type_radio ):
      return WidgetRadioButton(
        root        = root,
        label_text  = label_text,
        control_obj = control_obj
      )

#======================================================================#
#! /bin/python3

# screen_settings.py
# ------------------


class ScreenSettings:
  _gamma       = None
  _brightness  = None
  _screen_name = None

  @staticmethod
  def set_gamma( value ):
    ScreenSettings._gamma       = value

  @staticmethod
  def get_gamma():
    return ScreenSettings._gamma

  @staticmethod
  def set_brightness( value ):
    ScreenSettings._brightness  = value

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
    return f"xrandr --output {ScreenSettings.get_screen_name()} " + \
           f"--brightness {ScreenSettings.get_brightness()} "     + \
           f"--gamma {ScreenSettings.get_gamma()}:"               + \
           f"{ScreenSettings.get_gamma()}:"                       + \
           f"{ScreenSettings.get_gamma()}"
          

#======================================================================#
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

# Create an instance of the Brightness class
brightness = Brightness(
  get_config_option( "brightness", "screen_name"                        ),
  get_config_option( "brightness", "min_brightness",         0.0, float ),
  get_config_option( "brightness", "max_brightness",       100.0, float ),
  get_config_option( "brightness", "limit_min_brightness",  30.0, float ),
  get_config_option( "brightness", "limit_max_brightness", 100.0, float ),
  get_config_option( "brightness", "min_scaled_brightness",  0.0, float ),
  get_config_option( "brightness", "max_scaled_brightness",  1.0, float ),
  get_config_option( "brightness", "default_brightness",   100.0, float )
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
  get_config_option( "contrast", "default_contrast",   100.0, float )
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

# Prepare for brightness and contrast settings
ScreenSettings.set_screen_name( get_config_option( "contrast", "screen_name" ) )

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

#======================================================================#
#! /bin/python3

# mesure.py
# ---------

class Mesure:
  def __init__( self,
                val,
                offset,
                k,
                unit    ):
    """
    Initializes the Mesure object.
    
    :param val    : Normalized value
    :param offset : Offset for conversion
    :param k      : Scale factor
    :param unit   : Unit of measurement
    """
    self._val_norm = val
    self._offset   = offset
    self._k        = k
    self._unit     = unit

  def set_norm_val( self, val ):
    """Sets the normalized value."""
    self._val_norm = val

  def get_norm_val( self ):
    """Gets the normalized value."""
    return self._val_norm

  def set_val(self, val):
    """
    Sets the actual value, converting it to a normalized value.
    
    :param val: Actual value
    """
    self._val_norm  = ( val - self._offset ) / self._k

  def get_val( self ):
    """Gets the actual value from the normalized value."""
    return self._val_norm * self._k + self._offset

  def get_unit( self ):
    """Gets the unit of measurement."""
    return self._unit

  def pretty_print( self ):
    """Returns a formatted string of the actual value with its unit."""
    return f"{( self._val_norm * self._k + self._offset ):.2f} {self._unit}"

#======================================================================#
#! /bin/python3

# brightness.py
# -------------

import subprocess
import re
from   setting         import Setting
from   scale           import Scale
from   screen_settings import ScreenSettings


class Brightness( Setting, Scale ):
  def __init__( self,
                screen_name,
                min_value            =   0.0,
                max_value            = 100.0,
                limit_min_brightness =  30.0,
                limit_max_brightness = 100.0,
                min_scaled_value     =   0.0,
                max_scaled_value     =   1.0,
                default_value        = 100.0 ):
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
    self.screen_name      = screen_name

    # Prepare brightness regex
    self.brightness_regex = re.compile( r"Brightness: *?(\d\.?\d*)" )
    
    # Set default value
    self.set_value( default_value )
    


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
      # brightness_match = re.search( r"Brightness: *?(\d\.?\d*)", output )
      brightness_match = self.brightness_regex.search( r"Brightness: *?(\d\.?\d*)", output )
      if brightness_match:
        self.set_normalized_value( float( brightness_match.group(1) ) )
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
    ScreenSettings.set_brightness( self.get_norm_val() )
    try:
      # Construct the xrandr command to set the brightness
      command = ScreenSettings.get_command()
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

#======================================================================#
#! /bin/python3

# view.py
# -------

import tkinter       as tk
from tkinter         import ttk
from ttkthemes       import ThemedTk
from screen_settings import ScreenSettings
from widget          import *

class View:
  def __init__( self,
                brightness,
                sound_output,
                contrast,
                themes,
                default_theme ):
    self.root = ThemedTk( theme="arc" )  # Change the theme of the GUI
    self.root.title( "Settings Control" )

    self.brightness    = brightness
    self.sound_output  = sound_output
    self.contrast      = contrast
    
    self.themes        = themes.split( ',' )
    self.add_theme_to_menu()
    self.root.set_theme( default_theme )

    # Brightness Control
    brightness_widget   = WidgetBuilder.make(
      self.root,
      "Set Brightness:",
      self.brightness,
      WidgetBuilder.type_scale
    )
    ScreenSettings.set_brightness( self.brightness.get_norm_val() )

    # Contrast Control
    contrast_widget     = WidgetBuilder.make( 
      self.root,
      "Set Contrast:",
      self.contrast,
      WidgetBuilder.type_scale
    )
    ScreenSettings.set_gamma( self.contrast.get_norm_val() )

    # Sound Output Control
    sound_output_widget = WidgetBuilder.make( 
      self.root,
      "Set sound's output:",
      self.sound_output,
      WidgetBuilder.type_radio
    )

  def add_theme_to_menu( self ):
    menubar    = tk.Menu( self.root )
    theme_menu = tk.Menu( menubar, tearoff=0 )
    menubar.add_cascade( label="Themes", menu=theme_menu )

    for theme in self.themes:
      theme_menu.add_command(
        label   = theme,
        command = lambda
        t       = theme: self.root.set_theme(t)
      )
    self.root.config( menu=menubar )

  def run( self ):
    self.root.mainloop()

#======================================================================#
#! /bin/python3

# setting.py
# ----------

from abc import ABC, abstractmethod

class Setting( ABC ):
  """
  Abstract base class for settings.
  Defines the interface for getting and setting values.
  """

  @abstractmethod
  def get_current_value( self ):
    """
    Retrieves the current value of the setting.
    :return: The current value.
    """
    pass

  @abstractmethod
  def set_value( self, value ):
    """
    Sets the value of the setting.
    :param value: The value to set.
    """
    pass

#======================================================================#
#! /bin/python3

# scale.py
# --------

from abc    import ABC
from mesure import Mesure

class Scale( ABC ):
  def __init__( self, 
                min_value:        float,
                max_value:        float,
                limit_min_value:  float,
                limit_max_value:  float,
                unit:             str,
                scaled_min_value: float =   0.0,
                scaled_max_value: float =   1.0,
                default_value:    float = 100.0 ):
    """
    Initializes the Scale object.

    :param min_value       : Minimum scale value
    :param max_value       : Maximum scale value
    :param limit_min_value : Minimum limit value
    :param limit_max_value : Maximum limit value
    :param unit            : Unit of measurement
    """
    self.min             = min_value
    self.max             = max_value
    self.limit_min_value = limit_min_value
    self.limit_max_value = limit_max_value
    k                    = ( min_value - max_value ) / \
                           ( scaled_min_value - scaled_max_value )
    # min_value = scaled_min_value * k + offset
    offset               = min_value - scaled_min_value * k
    self._mesure         = Mesure( 
      max_value,
      offset,
      k,
      unit
    )
    
    # Set default value
    self.set_val( default_value )

  def get_min_value( self ) -> float:
    """Returns the minimum value."""
    return self.min

  def get_max_value( self ) -> float:
    """Returns the maximum value."""
    return self.max
  
  def get_limit_min_value( self ) -> float:
    """Returns the minimum limit value."""
    return self.limit_min_value

  def get_limit_max_value( self ) -> float:
    """Returns the maximum limit value."""
    return self.limit_max_value

  def set_normalized_value( self, value: float ) -> None:
    """Sets the normalized value."""
    self._mesure.set_norm_val( value )

  def get_norm_val( self ):
    """Gets the normalized value."""
    return self._mesure.get_norm_val()

  def get_val( self ):
    """Gets the actual value from the normalized value."""
    return self._mesure.get_val()

  def set_val( self, value: float ) -> None:
    """Sets the actual value, converting it to a normalized value."""
    self._mesure.set_val( value )

  def pretty_print( self ):
    """Returns a formatted string of the actual value with its unit."""
    return self._mesure.pretty_print()
