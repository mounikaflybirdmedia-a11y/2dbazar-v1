import os
import paramiko

# === SFTP SERVER DETAILS ===
HOST = "72.61.230.47"
PORT = 65002
USER = "u816361417_FPiWm2QlK"
PASS = "2Dbazaar@2026"

REMOTE_DIR = "/home/u816361417/websites/FPiWm2QlK/public_html" # Correct root directory based on SFTP test
LOCAL_DIR = "frontend"

def create_remote_dir(sftp, remote_directory):
    """Safely create directory on the remote server."""
    if remote_directory == '/':
        return
    if remote_directory == '':
        return
    try:
        sftp.stat(remote_directory)
    except IOError:
        # Create parent directories recursively
        parent = os.path.dirname(remote_directory)
        if parent:
            create_remote_dir(sftp, parent)
        try:
            sftp.mkdir(remote_directory)
        except IOError as e:
            print(f"Failed to create directory {remote_directory}: {e}")

def upload_directory(sftp, local_path, remote_path):
    print(f"Uploading {local_path} to {remote_path}...")
    create_remote_dir(sftp, remote_path)
    
    for item in os.listdir(local_path):
        local_item = os.path.join(local_path, item)
        # Force forward slashes for remote paths
        remote_item = f"{remote_path}/{item}"
        
        if os.path.isfile(local_item):
            print(f"  -> Uploading file: {item}")
            sftp.put(local_item, remote_item)
        elif os.path.isdir(local_item):
            upload_directory(sftp, local_item, remote_item)

import time

MAX_RETRIES = 5
RETRY_DELAY = 10

sftp = None
transport = None

for attempt in range(1, MAX_RETRIES + 1):
    try:
        print(f"Connecting to SFTP {HOST}:{PORT} (Attempt {attempt}/{MAX_RETRIES})...")
        transport = paramiko.Transport((HOST, PORT))
        transport.banner_timeout = 60
        transport.connect(username=USER, password=PASS)
        
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("Connection established successfully!")
        break
    except Exception as e:
        print(f"Connection attempt {attempt} failed: {e}")
        if transport:
            try:
                transport.close()
            except:
                pass
        if attempt < MAX_RETRIES:
            print(f"Waiting {RETRY_DELAY} seconds before retrying...")
            time.sleep(RETRY_DELAY)
        else:
            print("All connection attempts failed. Exiting.")
            exit(1)

try:
    upload_directory(sftp, LOCAL_DIR, REMOTE_DIR)
    sftp.close()
    transport.close()
    print("Upload complete! Frontend successfully deployed.")
except Exception as e:
    print(f"An error occurred during file upload: {e}")

