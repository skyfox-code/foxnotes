import os
import subprocess

STORAGE_DIR = "storage"

if __name__ == "__main__":
    os.makedirs(STORAGE_DIR, exist_ok=True)
    subprocess.Popen(["python", "app.py"])
