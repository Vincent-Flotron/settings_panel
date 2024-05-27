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
