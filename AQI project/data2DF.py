import requests
import pandas as pd

API_KEY = "579b464db66ec23bdd0000017d8cfdbec06044576442dd45e40399c2"
RESOURCE_ID = "3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"
API_URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}?api-key={API_KEY}&format=json&limit=1000"

def fetch_data_from_api():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        # Extract records and convert to DataFrame
        records = data.get('records', [])
        if not records:
            print("⚠️ No records found in response.")
            return

        df = pd.DataFrame(records)
        print(df.head())  # Preview first few rows
        return df

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return None

if __name__ == "__main__":
    df = fetch_data_from_api()

    if df is not None:
        # Optionally save to CSV
        df.to_csv("data_output.csv", index=False)
        print("✅ Data saved to 'data_output.csv'")

