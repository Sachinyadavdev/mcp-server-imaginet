import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        with open("schema.txt", "w") as f:
            for t in tables:
                t_name = list(t.values())[0]
                f.write(f"\n[{t_name}]\n")
                cursor.execute(f"DESCRIBE {t_name}")
                for col in cursor.fetchall():
                    f.write(f"  - {col['Field']} ({col['Type']})\n")
finally:
    conn.close()
