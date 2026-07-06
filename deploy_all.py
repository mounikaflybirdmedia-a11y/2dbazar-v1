import sys
sys.stdout.reconfigure(encoding='utf-8')
import paramiko
import os

HOST = "72.61.230.47"
PORT = 65002
USER = "u816361417_FPiWm2QlK"
PASS = "2Dbazaar@2026"

REMOTE_BASE = "/home/u816361417/websites/FPiWm2QlK/public_html"

import glob

FILES_TO_UPLOAD = []
# Add all frontend files recursively
for f in glob.glob(r"d:\2dbazar\frontend\**\*", recursive=True):
    if os.path.isfile(f):
        remote = f.replace(r"d:\2dbazar\frontend", REMOTE_BASE).replace("\\", "/")
        FILES_TO_UPLOAD.append((f, remote))



# Add the backend script
FILES_TO_UPLOAD.append((r"d:\2dbazar\backend\cleanup_session.php", f"{REMOTE_BASE}/api/cleanup_session.php"))

print(f"Connecting to {HOST}:{PORT}...\n")
transport = paramiko.Transport((HOST, PORT))
transport.connect(username=USER, password=PASS)
sftp = paramiko.SFTPClient.from_transport(transport)
print("Connected! Uploading files...\n")

for local, remote in FILES_TO_UPLOAD:
    if not os.path.exists(local):
        print(f"  [SKIP] Not found: {local}")
        continue
    try:
        sftp.put(local, remote)
        print(f"  [OK] {os.path.basename(local)}")
    except Exception as e:
        print(f"  [FAIL] {os.path.basename(local)}: {e}")

sftp.close()
transport.close()

print("\nDone! All files deployed.")
print(f"\nNEXT STEP - Run cleanup (removes old shared session from DB):")
print(f"  https://2dbazaar.com/api/cleanup_session.php")
print(f"  Then delete cleanup_session.php from server.")
