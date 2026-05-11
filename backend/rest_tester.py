import requests
import sys

def test_rest_api():
    ref = "chgmnyftxgtlgvplgeor"
    # Use the anon key from standard supabase structure if known, or service role
    # Wait, let's just try to GET root to see if we get 200 or 400
    url = f"https://{ref}.supabase.co/rest/v1/"
    
    print(f"Attempting REST ingress handshake on {url}...")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"!!! REST GATEWAY STATUS !!! => {response.status_code}")
        print("Success! The REST API is available via IPv4!")
        return True
    except Exception as e:
        print(f"REST GATEWAY FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    test_rest_api()
