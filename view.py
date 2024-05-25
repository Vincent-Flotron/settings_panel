#! /bin/python3

# view.py
# -------

import tkinter as tk
from   tkinter         import ttk
from   screen_settings import ScreenSettings

class Widget:
  def __init__(self, root, label_text, control_obj):
    self.root        = root
    self.control_obj = control_obj
    # Label for the widget
    self.label = ttk.Label(self.root, text=label_text)
    self.label.pack(pady=10)
    
    # Scale for the widget
    actual_value = control_obj.get_current_value()
    self.scale = ttk.Scale(
      self.root,
      from_   = control_obj.get_limit_min_value(),
      to      = control_obj.get_limit_max_value(),
      orient  = "horizontal",
      value   = actual_value if actual_value is not None else control_obj.get_norm_val(),
      command = self.on_scale_change
    )
    self.scale.pack(pady=20)
    
    # Display label for current value
    self.value_label = ttk.Label(self.root, text="")
    self.value_label.pack(pady=10)
    
    # Bind the scale event
    self.scale.bind("<ButtonRelease-1>", self.on_scale_release)
    self.update_value_label(actual_value)

      
  def update_value_label(self, value):
    self.value_label.config(text=f"Current Value: {value}")

  def on_scale_event(self):
    try:
      value = self.scale.get()
      if value != self.control_obj.get_val():
        self.control_obj.set_value(value)
        actual_value = self.control_obj.get_current_value()
        self.update_value_label(self.control_obj.pretty_print())
    except Exception as e:
      print(f"Error adjusting scale: {e}")
      self.update_value_label("Error adjusting scale")
      
  def on_scale_release(self, event):
    self.on_scale_event()
    
  def on_scale_change(self, event):
    self.on_scale_event()
    
def widget_builder(root, label_text, control_obj):
  return Widget(
    root        = root,
    label_text  = label_text,
    control_obj = control_obj
  )

class View:
    def __init__(self, brightness, sound_output, contrast):
        self.root = tk.Tk()
        self.root.title("Settings Control")

        self.brightness   = brightness
        self.sound_output = sound_output
        self.contrast     = contrast

        # Brightness Control
        brightness_widget = widget_builder( self.root, "Set Brightness:", self.brightness )
        ScreenSettings.set_brightness(self.brightness.get_norm_val())
        
        # Contrast Control
        contrast_widget   = widget_builder( self.root, "Set Contrast:",   self.contrast   )
        ScreenSettings.set_gamma(self.contrast.get_norm_val())
        
        # Sound Output Control
        self.sound_output_label = tk.ttk.Label(self.root, text="Select Sound Output:")
        self.sound_output_label.pack(pady=10)

        self.sound_output_var = tk.StringVar(value=self.sound_output.get_current_value())

        for option in self.sound_output.choices:
            rb = tk.ttk.Radiobutton(self.root, text=option, variable=self.sound_output_var, value=option, command=self.on_sound_output_change)
            rb.pack(anchor=tk.W)

    def update_output_sound(self, val):
        if val is not None:
            self.sound_output_label.config(text=f"Actual Output: {val}")
        else:
            self.sound_output_label.config(text="Unable to retrieve brightness")

    def on_sound_output_change(self):
        try:
            selected_output = self.sound_output_var.get()
            self.sound_output.set_value(selected_output)
        except Exception as e:
            print(f"Error changing sound output: {e}")
        self.update_output_sound(self.sound_output.get_current_value())

    def run(self):
        self.root.mainloop()
