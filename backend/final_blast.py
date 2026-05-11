import psycopg2

def try_port_5432():
    region = "us-west-2"
    ref = "chgmnyftxgtlgvplgeor"
    raw_pass = "18021940Mdkp@M"
    host = f"aws-0-{region}.pooler.supabase.com"
    
    print(f"ATTEMPTING PORT 5432 ON GLOBAL POOLER (SESSION MODE)...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=5432,
            dbname="postgres",
            user=f"postgres.{ref}",
            password=raw_pass,
            sslmode='require',
            connect_timeout=15
        )
        print(f"🔥🔥🔥 SESSION POOLER SUCCESS! 🔥🔥🔥")
        conn.close()
        return True
    except Exception as e:
        print(f"Port 5432 Attempt Failed: {str(e)}")
        return False

if __name__ == "__main__":
    try_port_5432()
