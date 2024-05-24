#! /bin/python3

# sound_output.py
# ---------------

from setting import Setting
import subprocess
import re

class SoundOutput(Setting):
    def __init__(self, choices, cards, card_outputs, configurations, outputs , ports):
        # self.output_options = ["Speakers", "HDMI", "Bluetooth"]
        self.choices        = choices.split(',')
        self.cards          = cards.split(',')
        self.card_outputs   = card_outputs.split(',')
        self.configurations = configurations.split(',')
        self.outputs        = outputs.split(',')
        self.ports          = ports.split(',')
        self.current_output = self.get_current_value()

    def get_current_value(self):
        try:
            # Get the actual profile used
            pactl_list_cards = subprocess.check_output("pactl list cards", shell=True, text=True).strip()
            profile_regex = r"Nom\s*:\s*" + re.escape(self.cards[0]) + r".*\r?\n(?:\t.*\r?\n)*\tProfil actif\s*:\s*output:(.+?)[\+|$]"
            actual_profil_match = re.search(profile_regex, pactl_list_cards)
            config_regex = r"Nom\s*:\s*" + re.escape(self.cards[0]) + r".*\r?\n(?:\t.*\r?\n)*\tProfil actif\s*:\s*(.+)"
            actual_config_match = re.search(config_regex, pactl_list_cards)
            
            if actual_profil_match:
                actual_profil = actual_profil_match.group(1).strip()
                print(f"actual_profil: {actual_profil}")
            else:
                raise ValueError("Failed to match actual profile.")
            
            if actual_config_match:
                actual_config = actual_config_match.group(1).strip()
                print(f"actual_config: {actual_config}")
            else:
                raise ValueError("Failed to match actual config.")

            # Get the actual port used
            pactl_list_sinks = subprocess.check_output("pactl list sinks", shell=True, text=True).strip()
            # print(f"pactl_list_sinks: {pactl_list_sinks}")
            # print(f"REGEX============================================")
            # print(r"Nom\s*:\s*" + f"{re.escape(self.card_outputs[0])}.{re.escape(actual_profil)}" + r".*\r?\n(?:\t.*\r?\n)*\tPort actif\s*:\s*(.+)")
            port_regex = r"Nom\s*:\s*" + f"{re.escape(self.card_outputs[0])}.{re.escape(actual_profil)}" + r".*\r?\n(?:\t.*\r?\n)*\tPort actif\s*:\s*(.+)"
            actual_port_match = re.search(port_regex, pactl_list_sinks)
            
            if actual_port_match:
                actual_port = actual_port_match.group(1).strip()
            else:
                raise ValueError("Failed to match actual port.")

            choice = self.find_choice_from(actual_config, actual_port)
            
            # Return the actual output (choice)
            # return (actual_profil, actual_port, choice)
            return choice

        except subprocess.CalledProcessError as e:
            print(f"Failed to get current sound output: {e}")
            return "Speakers"  # Default value on error
        except ValueError as e:
            print(e)
            return "Speakers"  # Default value on error
            

    def find_choice_from(self, config, port):
      print(f"Configs: {self.configurations}")
      try:
        conf_ind = self.configurations.index(config)
      except ValueError:
        print("config", config, "not found in the configuration list.")
        return None
      print(f"Ports: {self.ports}")
      try:
        port_ind = self.ports.index(port)
      except ValueError:
        print("port", port, "not found in the port list.")
        return None
      if (conf_ind == port_ind):
        return self.choices[port_ind]
    
    def find_choice_index(self, choice):
      try:
        choice_ind = self.choices.index(choice)
      except ValueError:
        print("choice", choice, "not found in the choice list.")
        return None
      return choice_ind

      
    def set_value(self, value):
        print(f"set_value. Value; {value}, choices; {self.choices}")
        if value in self.choices:
            choice_index    = self.find_choice_index(value)
            cmd_set_profile = f"pactl set-card-profile {self.cards[choice_index]} {self.configurations[choice_index]}"
            cmd_set_port    = f"pactl set-sink-port {self.card_outputs[choice_index]}.{self.outputs[choice_index]} {self.ports[choice_index]}"
            try:
                subprocess.run(cmd_set_profile, shell=True, check=True)
                self.current_output = value
            except subprocess.CalledProcessError as e:
                print(f"Failed to set sound output's profile: {e}")
            try:
                subprocess.run(cmd_set_port, shell=True, check=True)
                self.current_output = value
            except subprocess.CalledProcessError as e:
                print(f"Failed to set sound output's port: {e}")
