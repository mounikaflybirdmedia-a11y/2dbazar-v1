import sys
sys.stdout.reconfigure(encoding='utf-8')
import paramiko

HOST = "72.61.230.47"
PORT = 65002
USER = "u816361417_FPiWm2QlK"
PASS = "2Dbazaar@2026"

transport = paramiko.Transport((HOST, PORT))
transport.connect(username=USER, password=PASS)
sftp = paramiko.SFTPClient.from_transport(transport)

try:
    sftp.remove("/home/u816361417/websites/FPiWm2QlK/public_html/api/cleanup_session.php")
    print("[OK] cleanup_session.php deleted from server")
except Exception as e:
    print(f"[INFO] {e}")

sftp.close()
transport.close()
