#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime

SOURCE_DIR = "/path/to/source"                     # Directory to back up
BACKUP_NAME = f"backup_{datetime.now():%Y%m%d_%H%M%S}.tar.gz"
REMOTE_USER = "youruser"
REMOTE_HOST = "remote.server.com"
REMOTE_PATH = "/remote/backup/location/"

def create_archive():
    result = subprocess.run(
        ["tar", "-czf", BACKUP_NAME, "-C", SOURCE_DIR, "."],
        capture_output=True, text=True
    )
    return result.returncode == 0, result.stderr

def transfer_backup():
    result = subprocess.run(
        ["scp", BACKUP_NAME, f"{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}"],
        capture_output=True, text=True
    )
    return result.returncode == 0, result.stderr

def main():
    print(f"Creating backup for: {SOURCE_DIR}")
    success, error = create_archive()

    if not success:
        print(f" Backup creation failed: {error}")
        return

    print(f"Backup archive created: {BACKUP_NAME}")
    print("Transferring to remote server...")

    success, error = transfer_backup()

    if success:
        print(f" Backup successfully uploaded to {REMOTE_HOST}")
    else:
        print(f" Backup upload failed: {error}")

    if os.path.exists(BACKUP_NAME):
        os.remove(BACKUP_NAME)

if __name__ == "__main__":
    main()

