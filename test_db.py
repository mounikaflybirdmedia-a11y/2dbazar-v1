import pymysql

HOST = "72.61.230.47"
USER = "u816361417_FPiWm2QlK_2dbazar"
PASS = "2Dbazar@2026!"
DB = "u816361417_FPiWm2QlK_2dbazar"

try:
    print(f"Connecting to MySQL database at {HOST}...")
    connection = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASS,
        database=DB,
        connect_timeout=10
    )
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        result = cursor.fetchone()
        print("Successfully connected to the database!")
        print(f"Database Version: {result[0]}")
        
        # Show all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"Tables in database: {[t[0] for t in tables]}")
        
    connection.close()
except Exception as e:
    print(f"Failed to connect: {e}")
    print("\nNote: Hostinger usually disables remote MySQL connections by default.")
    print("If this failed with a connection timeout or access denied, you need to go to Hostinger hPanel -> Databases -> Remote MySQL and allow your current IP address, or allow '%' for all IPs.")
