import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os

HOST = "72.61.230.47"
PORT = 65002
USER = "u816361417_FPiWm2QlK"
PASS = "2Dbazaar@2026"

REMOTE_BASE = "/home/u816361417/websites/FPiWm2QlK/public_html"

FILES_TO_UPLOAD = [
    (r"d:\2dbazar\frontend\pages\admin.html", f"{REMOTE_BASE}/pages/admin.html"),
    (r"d:\2dbazar\frontend\pages\dashboard-employer.html", f"{REMOTE_BASE}/pages/dashboard-employer.html"),
    (r"d:\2dbazar\frontend\pages\dashboard-seller.html", f"{REMOTE_BASE}/pages/dashboard-seller.html"),
    (r"d:\2dbazar\frontend\pages\dashboard-provider.html", f"{REMOTE_BASE}/pages/dashboard-provider.html"),
    (r"d:\2dbazar\frontend\pages\jobs.html", f"{REMOTE_BASE}/pages/jobs.html"),
    (r"d:\2dbazar\frontend\pages\marketplace.html", f"{REMOTE_BASE}/pages/marketplace.html"),
    (r"d:\2dbazar\frontend\pages\properties.html", f"{REMOTE_BASE}/pages/properties.html"),
    (r"d:\2dbazar\frontend\pages\services.html", f"{REMOTE_BASE}/pages/services.html")
]

try:
    print("Connecting to FTP...")
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
    print("\n✅ Deployment complete!")
except Exception as e:
    print(f"❌ Error: {e}")
