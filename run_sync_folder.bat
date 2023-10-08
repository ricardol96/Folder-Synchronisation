@echo off
set /p source=Enter source folder path: 
set /p replica=Enter replica folder path: 
set /p log_file=Enter log file path: 
set /p interval=Enter synchronization interval (in seconds): 
python sync_folder.py "%source%" "%replica%" "%log_file%" %interval%
pause
