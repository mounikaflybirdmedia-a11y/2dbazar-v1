import os
import paramiko

# === SFTP SERVER DETAILS ===
HOST = "72.61.230.47"
PORT = 65002
USER = "u816361417_FPiWm2QlK"
PASS = "2Dbazaar@2026"

REMOTE_DIR = "/home/u816361417/websites/FPiWm2QlK/public_html"
LOCAL_DIR = "frontend"

def create_remote_dir(sftp, remote_directory):
    if remote_directory == '/': return
    if remote_directory == '': return
    try:
        sftp.stat(remote_directory)
    except IOError:
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
        remote_item = f"{remote_path}/{item}"
        
        if os.path.isfile(local_item):
            print(f"  -> Uploading file: {item}")
            sftp.put(local_item, remote_item)
        elif os.path.isdir(local_item):
            upload_directory(sftp, local_item, remote_item)

try:
    print(f"Connecting to SFTP {HOST}:{PORT}...")
    transport = paramiko.Transport((HOST, PORT))
    transport.connect(username=USER, password=PASS)
    sftp = paramiko.SFTPClient.from_transport(transport)
    print("Connection established successfully!")
    
    upload_directory(sftp, LOCAL_DIR, REMOTE_DIR)
    
    sftp.close()
    transport.close()
    print("Upload complete! Backend API successfully deployed.")

except Exception as e:
    print(f"An error occurred: {e}")
