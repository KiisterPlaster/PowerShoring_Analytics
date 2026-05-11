import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def seed_supabase():
    # Hardcode direct IPv6 to bypass broken system DNS resolver
    # Notice we provide explicit host, port, dbname to bypass string parsing ambiguity
    try:
        print(f"Connecting directly to Supabase IPv6 address...")
        conn = psycopg2.connect(
            host="2600:1f14:b9e:7b02:3bdb:d6a0:14a3:6958",
            port=5432,
            dbname="postgres",
            user="postgres",
            password="18021940Mdkp@M"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        sql_path = r"e:\Hackthon\HackathonE+\PowerShoring_Analytics\infrastructure\init.sql"
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
            
        print("Connection established! Executing bootstrap SQL...")
        cur.execute(sql_content)
        print("SQL migration applied Successfully!")
        
        cur.execute("SELECT count(*) FROM clusters;")
        print(f"Confirmed {cur.fetchone()[0]} rows injected in 'clusters' table.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    seed_supabase()
