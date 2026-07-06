import sys
sys.stdout.reconfigure(encoding='utf-8')
import paramiko
import os

HOST = "72.61.230.47"
PORT = 65002
USER = "u816361417_FPiWm2QlK"
PASS = "2Dbazaar@2026"

print(f"Connecting to {HOST}:{PORT}...\n")
transport = paramiko.Transport((HOST, PORT))
transport.connect(username=USER, password=PASS)
sftp = paramiko.SFTPClient.from_transport(transport)
print("Connected!\n")

def explore(path, depth=0):
    indent = "  " * depth
    try:
        items = sftp.listdir(path)
        for item in items:
            full = path + '/' + item
            try:
                stat = sftp.stat(full)
                is_dir = (stat.st_mode & 0o40000) != 0
                print(f"{indent}{'[D]' if is_dir else '[F]'} {full}")
                if is_dir and depth < 3:
                    explore(full, depth+1)
            except:
                print(f"{indent}[?] {full}")
    except Exception as e:
        print(f"{indent}[ERR] {path}: {e}")

explore('/home/u816361417')

sftp.close()
transport.close()
