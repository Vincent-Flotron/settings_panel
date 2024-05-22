# concatenate.py
# --------------

is_first_file = True

# Open the file containing the list of files to concatenate
with open('files_to_concatenate.txt', 'r') as file_list:
    # For each file in the list
    for filename in file_list:
        # Remove the newline character from the filename
        filename = filename.strip()

        # Open the file to concatenate
        with open(filename, 'r') as file_to_concat:
            # Open the file where we're concatenating the files (main.py)
            if is_first_file:
                write_mode = 'w'
            else:
                write_mode = 'a'
            with open('main.py', write_mode) as main_file:
                # If it's not the first file, write the file separator to the main file
                if not is_first_file:
                    main_file.write('\n#================================================================================================#\n')
                # For each line in the file to concatenate
                for line in file_to_concat:
                    # Write the line to the main file
                    main_file.write(line)
                is_first_file = False
