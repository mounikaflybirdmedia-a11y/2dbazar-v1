import ftplib

FTP_HOST = "72.61.230.47"
FTP_PORT = 65002
FTP_USER = "u816361417_FPiWm2QlK"
FTP_PASS = "2Dbazaar@2026"

try:
    print(f"Connecting to {FTP_HOST}:{FTP_PORT}...")
    ftp = ftplib.FTP()
    ftp.connect(FTP_HOST, FTP_PORT)
    ftp.login(FTP_USER, FTP_PASS)
    print("Connection established successfully!")
    print("Current directory:", ftp.pwd())
    print("Directory listing:")
    ftp.dir()
    ftp.quit()
except Exception as e:
    print(f"An error occurred: {e}")
