import os
import pytest
from unittest.mock import patch
from sync_folder import SyncFolder

# Fixture to create temporary folders for testing
@pytest.fixture
def temp_folders(tmpdir):
    source = tmpdir.mkdir("source")
    replica = tmpdir.mkdir("replica")
    return str(source), str(replica)

def test_invalid_arguments():
    with pytest.raises(ValueError):
        SyncFolder(None, None, None, -1)

def test_source_folder_not_found():
    with pytest.raises(FileNotFoundError):
        SyncFolder("/nonexistent/source/folder", "replica", "log.txt", 1)

def test_invalid_log_file_path(temp_folders):
    source, replica = temp_folders

    with pytest.raises(ValueError):
        SyncFolder(source, replica, None, 1)

def test_synchronization_script(temp_folders):
    source, replica = temp_folders

    new_file_path = os.path.join(source, "new_file.txt")
    with open(new_file_path, "w") as f:
        f.write("Test content")

    with patch("shutil.copy2") as mock_copy:
        sync_folder = SyncFolder(source, replica, "log.txt", 1)
        sync_folder.synchronization()
        mock_copy.assert_called_once_with(new_file_path, os.path.join(replica, "new_file.txt"))

def test_file_modification(temp_folders):
    source, replica = temp_folders

    new_file_path = os.path.join(source, "new_file.txt")
    with open(new_file_path, "w") as f:
        f.write("Original content")

    replica_file_path = os.path.join(replica, "new_file.txt")
    with open(replica_file_path, "w") as f:
        f.write("Modified content")

    sync_folder = SyncFolder(source, replica, "log.txt", 1)
    sync_folder.synchronization()
    with open(replica_file_path, "r") as f:
        assert f.read() == "Original content"

def test_file_removal(temp_folders):
    source, replica = temp_folders
    replica_file_path = os.path.join(replica, "file_to_remove.txt")
    with open(replica_file_path, "w") as f:
        f.write("Content to be removed")

    sync_folder = SyncFolder(source, replica, "log.txt", 1)
    sync_folder.synchronization()
    assert not os.path.exists(replica_file_path)
