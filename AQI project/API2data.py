import requests

API_KEY = "579b464db66ec23bdd0000017d8cfdbec06044576442dd45e40399c2"
RESOURCE_ID = "3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"
API_URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}?api-key={API_KEY}&format=json&limit=1000"

def fetch_data_from_api():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        # DEBUG: print full response
        import json
        print(json.dumps(data, indent=2))

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")


if __name__ == "__main__":
    fetch_data_from_api()
