import os
import pandas as pd
import requests

# Bounding box over Kenyan airspace for flight tracking (min_lat, max_lat, min_lon, max_lon)
PARAMS = {
    "lamin": -4.7,   # Southernmost point (near Lungalunga/Vanga)
    "lamax": 4.7,    # Northernmost point (near the Ilemi Triangle/Ethio-Kenyan border)
    "lomin": 33.9,   # Westernmost point (Lake Victoria/Ugandan border)
    "lomax": 41.9    # Easternmost point (Somali border intersection at Mandera)
}

URL = "https://opensky-network.org/api/states/all"
file_dir = "data"
file_path = os.path.join(file_dir, "live_flights.csv")

try:
    response = requests.get(URL, params=PARAMS)
    response.raise_for_status()
    
    raw_data = response.json()
    columns = [
        "icao24", "callsign", "origin_country", "time_position", 
        "last_contact", "longitude", "latitude", "baro_altitude", 
        "on_ground", "velocity", "true_track", "vertical_rate", 
        "sensors", "geo_altitude", "squawk", "spi", "position_source"
    ]

    if raw_data.get("states"):
        df = pd.DataFrame(raw_data["states"], columns=columns)
        target_df = df[["icao24", "callsign", "longitude", "latitude", "baro_altitude", "on_ground", "velocity"]]
        
        # Create file directory if it doesn't already exist
        os.makedirs(file_dir, exist_ok=True)
        # Check if file exists to determine if we write headers
        file_exists = os.path.exists(file_path)
        
        # Open in append mode ('a')
        target_df.to_csv(file_path, mode='a', index=False, header=not file_exists)
        print(f"Appended {len(target_df)} new aircraft records to {file_path}.")
    else:
        print("Airspace is completely empty right now. No data to append.")

except Exception as e:
    print(f"Telemetry ingestion failed: {e}")
    exit(1)