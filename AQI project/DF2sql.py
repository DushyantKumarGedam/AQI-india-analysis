import pandas as pd
import mysql.connector


# === Step 1: Load and Clean CSV ===
df = pd.read_csv("data_output.csv")

# Convert 'last_update' to datetime (invalid ones become NaT)
df['last_update'] = pd.to_datetime(df['last_update'], format="%d-%m-%Y %H:%M:%S", errors='coerce')

# Replace NaN, NaT, and string 'nan' with None (MySQL uses NULL)
df = df.replace({pd.NaT: None, pd.NA: None, float('nan'): None, 'nan': None})
df = df.where(pd.notnull(df), None)

# === Step 2: Connect to MySQL ===
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='', # write your sql password here
    database='aqi_data'
)

cursor = conn.cursor()

# === Step 3: Create Table if Not Exists ===
cursor.execute("""
CREATE TABLE IF NOT EXISTS air_quality_data (
    country VARCHAR(50),
    state VARCHAR(50),
    city VARCHAR(100),
    station VARCHAR(150),
    last_update DATETIME,
    latitude DOUBLE,
    longitude DOUBLE,
    pollutant_id VARCHAR(20),
    min_value FLOAT,
    max_value FLOAT,
    avg_value FLOAT
)
""")

# === Step 4: Insert Data ===
insert_query = """
INSERT INTO air_quality_data (
    country, state, city, station, last_update,
    latitude, longitude, pollutant_id,
    min_value, max_value, avg_value
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for i, row in df.iterrows():
    try:
        cursor.execute(insert_query, (
            row['country'],
            row['state'],
            row['city'],
            row['station'],
            row['last_update'],
            row['latitude'],
            row['longitude'],
            row['pollutant_id'],
            row['min_value'],
            row['max_value'],
            row['avg_value']
        ))
    except Exception as e:
        print(f"❌ Error at row {i}: {row.to_dict()}")
        print(f"Exception: {e}")
        break  # Or use `continue` if you want to skip bad rows

cursor.execute("SELECT * FROM air_quality_data")
rows = cursor.fetchall()
# === Step 5: Finalize ===
conn.commit()
cursor.close()
conn.close()
print("✅ Data insertion completed successfully.")
