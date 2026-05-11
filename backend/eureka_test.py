import psycopg2

def check_pure():
    host = "aws-1-us-west-2.pooler.supabase.com"
    ref = "chgmnyftxgtlgvplgeor"
    raw_pass = "18021940Mdkp@M"
    
    print("TESTING AWS-1 NODE...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=6543,
            dbname="postgres",
            user=f"postgres.{ref}",
            password=raw_pass,
            sslmode='require',
            connect_timeout=10
        )
        print("--- [SUCCESS] CONNECTED TO DATABASE SUCCESSFULLY! ---")
        
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM clusters;")
        count = cur.fetchone()[0]
        print("VERIFIED RECORD COUNT: " + str(count))
        conn.close()
        return True
    except Exception as e:
        print("FAILED FINAL ATTEMPT: " + str(e))
        return False

if __name__ == "__main__":
    check_pure()
