import psycopg2

def cert_validated_blast():
    region = "us-west-2"
    ref = "chgmnyftxgtlgvplgeor"
    raw_pass = "18021940Mdkp@M"
    
    host = f"aws-0-{region}.pooler.supabase.com"
    # Path to certificate we just saved
    cert_path = r"e:\Hackthon\HackathonE+\PowerShoring_Analytics\backend\supabase.crt"
    
    print(f"ATTEMPTING SECURE SSL HANDSHAKE WITH CUSTOM CA CERTIFICATE...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=6543,
            dbname="postgres",
            user=f"postgres.{ref}",
            password=raw_pass,
            sslmode='verify-full', # Force Full Validation with our provided cert
            sslrootcert=cert_path,
            connect_timeout=15
        )
        print(f"🔥🔥🔥🔥 CERTIFICATE VALIDATION SUCCESS!!! CONNECTED!!! 🔥🔥🔥🔥")
        
        conn.autocommit = True
        cur = conn.cursor()
        sql_path = r"e:\Hackthon\HackathonE+\PowerShoring_Analytics\infrastructure\init.sql"
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
            
        print("Pushing full infrastructure bootstrap payloads via verified tunnel...")
        cur.execute(sql_content)
        
        cur.execute("SELECT count(*) FROM clusters;")
        total = cur.fetchone()[0]
        print(f"SUCCESS! Schema fully flushed. Active data points verified: {total}")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Cert Verification Failed: {str(e)}")
        return False

if __name__ == "__main__":
    cert_validated_blast()
