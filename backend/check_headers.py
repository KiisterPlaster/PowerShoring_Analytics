import requests
url = "https://chgmnyftxgtlgvplgeor.supabase.co/rest/v1/"
try:
    resp = requests.get(url, timeout=10)
    print(f"Status: {resp.status_code}")
    print("Headers:")
    for k, v in resp.headers.items():
        print(f"  {k}: {v}")
except Exception as e:
    print(f"Error: {e}")
