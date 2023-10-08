import os
import shutil
import sys
import time
import hashlib

class SyncFolder:

    def __init__(self, source, replica, log_file, interval):
        self.source = source
        self.replica = replica
        self.log_file = log_file
        self.interval = interval

        if any(not arg for arg in (source, replica, log_file, interval)):
            raise ValueError("Invalid arguments provided. Command usage: python folder_sync.py <source_folder_path> <replica_folder_path> <log_file> <interval>")
        
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source folder not found: {source}")
        
        try:
            self.interval = int(interval)
            if self.interval <= 0:
                raise ValueError("Interval must be a positive integer.")
        except ValueError:
            raise ValueError("Interval must be a positive integer.")
        
        

    def main(self):
        try:
            while True:
                self.logging("Synchronization started.")
                self.synchronization()
                self.logging("Synchronization completed.")
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.logging("Synchronization interrupted.")

    def logging(self, message):
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    def synchronization(self):
        source_files = set()
        replica_files = set()

        # Set of files in source dir
        for folder, _, files in os.walk(self.source):
            for file in files:
                source_files.add(os.path.relpath(os.path.join(folder, file), self.source))

        # Set of files in replica dir
        for folder, _, files in os.walk(self.replica):
            for file in files:
                replica_files.add(os.path.relpath(os.path.join(folder, file), self.replica))

        new_files = source_files - replica_files
        modified_files = {file for file in source_files if self.is_modified(file)}
        deleted_files = replica_files - source_files

        # New files
        for file in new_files:
            source_file_path = os.path.join(self.source, file)
            replica_file_path = os.path.join(self.replica, file)
            os.makedirs(os.path.dirname(replica_file_path), exist_ok=True)
            shutil.copy2(source_file_path, replica_file_path)
            self.logging(f"New File Created: {replica_file_path}")

        # Modified files
        for file in modified_files:
            source_file_path = os.path.join(self.source, file)
            replica_file_path = os.path.join(self.replica, file)
            os.makedirs(os.path.dirname(replica_file_path), exist_ok=True)
            shutil.copy2(source_file_path, replica_file_path)
            self.logging(f"File Modified: {replica_file_path}")


        # Removed files
        for file in deleted_files:
            replica_file_path = os.path.join(self.replica, file)
            os.remove(replica_file_path)
            self.logging(f"File Removed: {replica_file_path}")

    def is_modified(self, file):
        # check if md5 hash has changed between source and replica files
        source_file_path = os.path.join(self.source, file)
        replica_file_path = os.path.join(self.replica, file)

        if os.path.exists(source_file_path) and os.path.exists(replica_file_path):
            return self.calculate_md5(source_file_path) != self.calculate_md5(replica_file_path)
        else:
            return False

    def calculate_md5(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

if __name__ == "__main__":
    # cmd arguments
    source = sys.argv[1]
    replica = sys.argv[2]
    log_file = sys.argv[3]
    interval = sys.argv[4]

    if not os.path.exists(replica):
        os.makedirs(replica)
    
    sync_folder = SyncFolder(source, replica, log_file, interval)
    sync_folder.main()
