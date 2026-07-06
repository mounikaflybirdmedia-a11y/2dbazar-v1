import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os

HOST = "72.61.230.47"
PORT = 65002
USER = "u816361417_FPiWm2QlK"
PASS = "2Dbazaar@2026"

REMOTE_BASE = "/home/u816361417/domains/2dbazaar.com/public_html"

FILES_TO_UPLOAD = [
    # (local_path, remote_path)
    (r"d:\2dbazar\frontend\js\data.js",           f"{REMOTE_BASE}/frontend/js/data.js"),
    (r"d:\2dbazar\backend\cleanup_session.php",   f"{REMOTE_BASE}/api/cleanup_session.php"),
]

try:
    transport = paramiko.Transport((HOST, PORT))
    transport.connect(username=USER, password=PASS)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    for local, remote in FILES_TO_UPLOAD:
        if os.path.exists(local):
            sftp.put(local, remote)
            print(f"✅ Uploaded: {os.path.basename(local)} → {remote}")
        else:
            print(f"❌ File not found: {local}")
    
    sftp.close()
    transport.close()
    print("\n✅ Done! Now visit: https://2dbazaar.com/api/cleanup_session.php")
    print("   Then DELETE cleanup_session.php from server after running it.")
except Exception as e:
    print(f"❌ Error: {e}")
