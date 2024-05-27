#! /bin/python3

# widget.py
# ---------

import tkinter as tk
from   tkinter import ttk

class Widget:
  def __init__( 
                self,
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
  def __init__(
                self,
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
    super().update_value_label( actual_value )

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
  def __init__( 
                self,
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
