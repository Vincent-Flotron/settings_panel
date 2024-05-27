#! /bin/python3

import re

def extract_files( main_file_path ):
  with open( main_file_path, 'r' ) as main_file:
    content  = main_file.read()
    sections = content.split( '#================================================================================================#\n' )

  for i in range( 0, len( sections ) ):  # start from 1 to skip the first section which is empty
    section_content = sections[i]
    file_match      = re.search( '# *([-_\w]+.py)\n# *-{10,} *\n', section_content )  # use the capture group of the provided regex

    if file_match:  # make sure there's a match
      file_name = file_match.group(1)  # extract the file name
      with open( file_name, 'w' ) as extracted_file:
        extracted_file.write( section_content )  # write the content of the section, skipping the first three lines

extract_files('main.py')
