import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.environ.get("DATABASE_URL")

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'detections' AND column_name = 'id';
    """)
    res = cur.fetchone()
    print(f"Column info: {res}")
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")
