#! /bin/python3

# concatenate_lister.py
# ---------------------

import os

# Specify the directory path
dir_path = '.'

# Open the file where we'll write the list of files
with open( 'files_to_concatenate.txt', 'w' ) as file_list:
  # For each file in the directory
  for filename in os.listdir( dir_path ):
    # If the file ends with '.py' and is not 'concatenate.py' or 'concatenate_lister.py'
    if filename.endswith( '.py' ) \
      and filename not in [ 'concatenate.py',              \
                            'concatenate_lister.py',       \
                            'update_from_concatenated.py', \
                            'update_from_main.py',         \
                            'puissance.py',                \
                            'gamma_formula.py'             ]:
      # Write the file name to the file list
      file_list.write( filename + '\n' )
