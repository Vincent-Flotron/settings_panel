#! /bin/python3

# view.py
# -------

import tkinter       as tk
from tkinter         import ttk
from ttkthemes       import ThemedTk
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

    # Contrast Control
    contrast_widget     = WidgetBuilder.make( 
      self.root,
      "Set Contrast:",
      self.contrast,
      WidgetBuilder.type_scale
    )

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
