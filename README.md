# Folder-Synchronisation
If you don't have pytest installed simply install it using
pip install pytest

To use this program simply run the run_sync_folder.bat if using Windows or run run_sync_folder.sh if using Linux
The launcher will prompt you to input the following arguments:

source - Path to the source directory
replica - Path to the replica folder (if folder doesn't exist it will automatically create a directory)
log_file - It will create log file in the same directory as the project
interval - The interval (in seconds) in which the program will run

All actions File creation/File removal/ File modification will be logged in the log file.

To stop the Synchronization program simply press Ctrl+C
