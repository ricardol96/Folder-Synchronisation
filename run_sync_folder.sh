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

# chmod +x run_sync_folder.sh

# Run the main script with user input as command-line arguments
python sync_folder.py "$source" "$replica" "$log_file" "$interval"
read -p "Press Enter to exit..."