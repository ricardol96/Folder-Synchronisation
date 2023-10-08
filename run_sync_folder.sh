#!/bin/bash

# Prompt the user for input
echo "Enter source folder path:"
read source

echo "Enter replica folder path:"
read replica

echo "Enter log file path:"
read log_file

echo "Enter interval:"
read interval

# Run the unit tests
pytest unit_test.py

# Run the chmod command to make the script self-executable
chmod +x run_unit_tests.sh

# Run the main script with user input as command-line arguments
python sync_folder.py "$source" "$replica" "$log_file" "$interval"
