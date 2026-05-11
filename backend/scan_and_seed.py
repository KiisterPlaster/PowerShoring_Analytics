import psycopg2
import time

regions = [
    "sa-east-1", # Sao Paulo (High chance!)
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
    "eu-central-1",
    "eu-west-1",
    "ap-southeast-1"
]

# Correct pooler syntax requires postgres.project_ref as the username
username = "postgres.chgmnyftxgtlgvplgeor"
password = "18021940Mdkp@M"
dbname = "postgres"

print("Auto-scanning AWS Pooler Regions to bypass local IPv6 networking limitation...")
found = False

for reg in regions:
    host = f"aws-0-{reg}.pooler.supabase.com"
    print(f"Scanning region {reg} at {host}...", end=' ', flush=True)
    try:
        # Use port 6543 for transaction pooler (IPv4 safe) or 5432 if session mode supported
        conn = psycopg2.connect(
            host=host,
            port=6543, 
            dbname=dbname,
            user=username,
            password=password,
            connect_timeout=5
        )
        print("SUCCESS! Found Region Match!")
        print(f"\n>>> WINNING REGION: {reg}")
        
        # Execute Init immediately since we are connected!
        conn.autocommit = True
        cur = conn.cursor()
        sql_path = r"e:\Hackthon\HackathonE+\PowerShoring_Analytics\infrastructure\init.sql"
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print("Executing Database Bootstrap...")
        cur.execute(sql_content)
        
        cur.execute("SELECT count(*) FROM clusters;")
        res = cur.fetchone()[0]
        print(f"Bootstrap COMPLETE. Confirmed {res} cluster records injected!")
        
        cur.close()
        conn.close()
        found = True
        break
    except Exception as e:
        print(f"Failed: {str(e)}")

if not found:
    print("\nCRITICAL ERROR: Exhausted known common AWS regions. Could not find valid pooler gateway.")
