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
    self._val_norm = ( val - self._offset ) / self._k

  def get_val( self ):
    """Gets the actual value from the normalized value."""
    return self._val_norm * self._k + self._offset

  def get_unit( self ):
    """Gets the unit of measurement."""
    return self._unit

  def pretty_print( self ):
    """Returns a formatted string of the actual value with its unit."""
    return f"{( self._val_norm * self._k + self._offset ):.2f} {self._unit}"
