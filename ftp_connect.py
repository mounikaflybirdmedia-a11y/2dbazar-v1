import sys
sys.stdout.reconfigure(encoding='utf-8')
import paramiko
import socket

# Hostinger standard SSH configs to try
CONFIGS = [
    {"host": "srv547.hstgr.io", "port": 65002},
    {"host": "72.61.230.47",    "port": 65002},
    {"host": "72.61.230.47",    "port": 22},
    {"host": "srv547.hstgr.io", "port": 22},
]

USER = "u816361417_FPiWm2QlK"
PASS = "2Dbazaar@2026"

def test_port(host, port, timeout=5):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((host, port))
        banner = s.recv(256).decode(errors='ignore')
        s.close()
        return True, banner.strip()
    except Exception as e:
        return False, str(e)

print("Step 1: Testing TCP connectivity...\n")
for cfg in CONFIGS:
    ok, msg = test_port(cfg['host'], cfg['port'])
    status = "OPEN" if ok else "CLOSED/BLOCKED"
    print(f"  {cfg['host']}:{cfg['port']} -> {status}")
    if ok:
        print(f"    Banner: {msg[:80]}")

print("\nStep 2: Trying SFTP auth on open ports...\n")
for cfg in CONFIGS:
    ok, _ = test_port(cfg['host'], cfg['port'])
    if not ok:
        continue
    try:
        transport = paramiko.Transport((cfg['host'], cfg['port']))
        transport.connect(username=USER, password=PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print(f"[SUCCESS] {cfg['host']}:{cfg['port']}")
        try:
            print("  Home:", sftp.listdir('/home/u816361417'))
        except:
            print("  Connected but can't list /home")
        sftp.close()
        transport.close()
        break
    except paramiko.AuthenticationException:
        print(f"[AUTH FAIL] {cfg['host']}:{cfg['port']} - wrong password")
    except Exception as e:
        print(f"[SSH FAIL] {cfg['host']}:{cfg['port']} - {e}")
