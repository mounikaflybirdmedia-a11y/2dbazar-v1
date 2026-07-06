import paramiko

HOST = "72.61.230.47"
PORT = 65002
USER = "u816361417_FPiWm2QlK"
PASS = "2Dbazaar@2026"

try:
    print(f"Connecting to SSH {HOST}:{PORT}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=HOST, port=PORT, username=USER, password=PASS)
    
    print("SSH Connection established successfully!")
    
    # We write a simple PHP script to test the DB connection
    php_code = """
<?php
$servername = "localhost";
$username = "u816361417_FPiWm2QlK_2dbazar";
$password = "2Dbazar@2026!";
$dbname = "u816361417_FPiWm2QlK_2dbazar";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully via PHP on the server!";
?>
"""
    
    # Run the PHP code directly using the PHP CLI
    # We pipe the code to php
    command = f'php -r \'{php_code}\''
    
    print("Running PHP test on the server...")
    stdin, stdout, stderr = client.exec_command('php -v; cat << "EOF" > test_db.php\n' + php_code + '\nEOF\nphp test_db.php')
    
    print("OUTPUT:")
    print(stdout.read().decode())
    print("ERRORS:")
    print(stderr.read().decode())
    
    client.close()
except Exception as e:
    print(f"An error occurred: {e}")
