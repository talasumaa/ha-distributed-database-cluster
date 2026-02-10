import mysql.connector
import time
import sys
from datetime import datetime

# CONFIGURATION
DB_CONFIG = {
    'user': 'root',
    'password': 'password',  # Change this to match your setup
    'host': '192.168.205.70', # The Floating IP
    'database': 'test_db',
    'connection_timeout': 2
}

def log_status(status, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] [{status}] {message}")
    # Also append to file for evidence
    with open("../evidence/failover_log.txt", "a") as f:
        f.write(f"[{timestamp}] [{status}] {message}\n")

def run_test():
    print("--- Starting High-Availability Chaos Monitor ---")
    print(f"Targeting VIP: {DB_CONFIG['host']}")
    
    while True:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Identify which physical node we are talking to
            cursor.execute("SELECT @@hostname")
            result = cursor.fetchone()
            hostname = result[0] if result else "UNKNOWN"
            
            log_status("SUCCESS", f"Connected to {hostname}")
            conn.close()
            
        except mysql.connector.Error as err:
            log_status("FAILURE", f"Connection Lost: {err}")
        except Exception as e:
            log_status("ERROR", f"System Error: {e}")
            
        time.sleep(0.5) # Poll every 500ms

if __name__ == "__main__":
    # Ensure evidence dir exists
    import os
    if not os.path.exists("../evidence"):
        os.makedirs("../evidence")
    
    # Create DB if not exists (One time setup manually preferred, but this handles simple checks)
    run_test()