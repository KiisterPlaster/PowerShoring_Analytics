import requests
import json

def test_rest_fetch():
    ref = "chgmnyftxgtlgvplgeor"
    url = f"https://{ref}.supabase.co/rest/v1/clusters?select=*"
    
    # The Secret Key I found in the user image!
    secret_key = "sb_secret_A3fdtjM0cYnwWoK19EPiCjg_vQsbw0Eq"
    
    headers = {
        "apikey": secret_key,
        "Authorization": f"Bearer {secret_key}"
    }
    
    print(f"Fetching clusters via HTTP REST API from {url}...")
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            print(f"🔥 SUCCESS!!! REST API Returned {len(data)} records!")
            print("Sample record name:", data[0]['name'] if data else "No data yet")
            return True
        else:
            print(f"REST Auth Failed. Status: {r.status_code}")
            print(f"Body: {r.text}")
            return False
    except Exception as e:
        print(f"REST API Exception: {str(e)}")
        return False

if __name__ == "__main__":
    test_rest_fetch()
