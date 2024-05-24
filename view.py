#! /bin/python3

# view.py
# -------

import tkinter as tk
from tkinter import ttk

class View:
    def __init__(self, brightness, sound_output):
        self.root = tk.Tk()
        self.root.title("Settings Control")

        self.brightness   = brightness
        self.sound_output = sound_output

        # Brightness Control
        actual_value = self.brightness.get_current_value()
        label = tk.ttk.Label(self.root, text="Set Brightness:")
        label.pack(pady=10)

        self.brightness_scale = tk.ttk.Scale(
            self.root,
            from_=self.brightness.get_limit_min_value(),
            to=self.brightness.get_limit_max_value(),
            orient="horizontal",
            value=actual_value if actual_value is not None else self.brightness.get_norm_val(),
            command=self.on_brightness_scale_change
        )
        self.brightness_scale.pack(pady=20)

        self.brightness_label = tk.ttk.Label(self.root, text="")
        self.brightness_label.pack(pady=10)

        self.brightness_scale.bind("<ButtonRelease-1>", self.on_brightness_scale_release)
        self.update_brightness_label(actual_value)

        # Sound Output Control
        self.sound_output_label = tk.ttk.Label(self.root, text="Select Sound Output:")
        self.sound_output_label.pack(pady=10)

        self.sound_output_var = tk.StringVar(value=self.sound_output.get_current_value())

        for option in self.sound_output.choices:
            rb = tk.ttk.Radiobutton(self.root, text=option, variable=self.sound_output_var, value=option, command=self.on_sound_output_change)
            rb.pack(anchor=tk.W)

    def on_brightness_scale_release(self, event):
        try:
            value = self.brightness_scale.get()
            if value != self.brightness.get_val():
                self.brightness.set_value(value)
                actual_value = self.brightness.get_current_value()
                self.update_brightness_label(actual_value)
        except Exception as e:
            print(f"Error adjusting brightness: {e}")
            self.brightness_label.config(text="Error adjusting brightness")

    def on_brightness_scale_change(self, value):
        try:
            value = float(value)
            if value != self.brightness.get_val():
                self.brightness.set_value(value)
                actual_value = self.brightness.get_current_value()
                self.update_brightness_label(actual_value)
        except Exception as e:
            print(f"Error adjusting brightness: {e}")
            self.brightness_label.config(text="Error adjusting brightness")

    def update_brightness_label(self, val):
        if val is not None:
            self.brightness_label.config(text=f"Actual Brightness: {self.brightness.pretty_print()}")
        else:
            self.brightness_label.config(text="Unable to retrieve brightness")
            
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
