import psycopg2
import sys
import os

# Fix encoding for print
os.environ["PYTHONIOENCODING"] = "utf-8"

def scan_all_regions():
    ref = "chgmnyftxgtlgvplgeor"
    raw_pass = "18021940Mdkp@M"
    user = f"postgres.{ref}"
    
    regions = [
        "us-west-2", # Expected from screenshot
        "sa-east-1", # Highly probable due to Hackathon location (Brazil)
        "us-east-1", # Extremely common fallback
        "us-west-1", # Close to oregon
        "eu-central-1"
    ]
    
    print(f"--- COMMENCING GLOBAL POOLER SCAN FOR TENANT '{ref}' ---")
    
    found_working = None
    
    for region in regions:
        host = f"aws-0-{region}.pooler.supabase.com"
        print(f"Scanning {region}...")
        
        for port in [6543, 5432]:
            try:
                conn = psycopg2.connect(
                    host=host,
                    port=port,
                    dbname="postgres",
                    user=user,
                    password=raw_pass,
                    sslmode='require',
                    connect_timeout=5
                )
                print(f"!!! SUCCESSFUL CONNECTION !!! REGION: {region} | PORT: {port}")
                conn.close()
                found_working = (region, port)
                break
            except Exception as e:
                error_str = str(e).strip().replace("\n", " ")
                if "tenant/user" in error_str and "not found" in error_str:
                     pass # Silent proceed to next port/region
                elif "password authentication failed" in error_str:
                     print(f"-> {region} (PORT {port}): TENANT FOUND! AUTH ISSUE (PROBABLY REAL ENDPOINT!)")
                     found_working = (region, port)
                     break
                else:
                     pass
        if found_working:
             break

    if found_working:
         print(f"\n[FINAL] WINNER REGION: {found_working[0]} | PORT: {found_working[1]}")
    else:
         print(f"\n[FINAL] All global edge routers returned ENOTFOUND. The pooler is not provisioned.")

if __name__ == "__main__":
    scan_all_regions()
