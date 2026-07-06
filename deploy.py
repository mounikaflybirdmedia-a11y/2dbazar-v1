import os
import ftplib

# === FTP SERVER DETAILS ===
FTP_HOST = "ftp.yourdomain.com"
FTP_USER = "your_username"
FTP_PASS = "your_password"
FTP_DIR = "/public_html" # Target directory on the server

# The local folder you want to upload (e.g., 'frontend')
LOCAL_DIR = "frontend"

def create_ftp_dir(ftp, dir_path):
    """Safely create directories on the FTP server."""
    dirs = dir_path.split('/')
    for d in dirs:
        if not d: continue
        try:
            ftp.cwd(d)
        except ftplib.error_perm:
            try:
                ftp.mkd(d)
                ftp.cwd(d)
            except ftplib.error_perm as e:
                print(f"Failed to create directory {d}: {e}")

def upload_directory(ftp, local_path, remote_path):
    print(f"Uploading {local_path} to {remote_path}...")
    ftp.cwd("/")
    create_ftp_dir(ftp, remote_path)
    
    for item in os.listdir(local_path):
        local_item = os.path.join(local_path, item)
        remote_item = f"{remote_path}/{item}"
        
        if os.path.isfile(local_item):
            print(f"  -> Uploading file: {item}")
            with open(local_item, 'rb') as f:
                ftp.storbinary(f'STOR {item}', f)
        elif os.path.isdir(local_item):
            upload_directory(ftp, local_item, remote_item)
            ftp.cwd("..")

try:
    print(f"Connecting to {FTP_HOST}...")
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    print("Connection established successfully!")
    
    upload_directory(ftp, LOCAL_DIR, FTP_DIR)
    
    ftp.quit()
    print("Upload complete!")

except Exception as e:
    print(f"An error occurred: {e}")
