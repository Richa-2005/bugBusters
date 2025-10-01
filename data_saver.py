# data_saver.py
import json
import time
import os
from datetime import datetime

from geo_module import get_city_coords

def update_and_save_data(city_name, file_path="city_coords_log.json"):
    """
    Fetches coordinates for a city and appends them to a JSON file.
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching coordinates for {city_name}...")
    
    new_coords_dict = get_city_coords(city_name)
    
    if new_coords_dict is None:
        print("Failed to get coordinates, skipping update.")
        return

    data = {}
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("Warning: JSON file is corrupt or empty. Starting with a new structure.")
                data = {}
    
    if city_name not in data:
        data[city_name] = []
        
    data[city_name].append({
        "coordinates": [new_coords_dict["latitude"], new_coords_dict["longitude"]],
        "timestamp": datetime.now().isoformat()
    })

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    
    print(f"Successfully updated and saved data for {city_name}.")

def run_scheduler(city_to_track):
    """
    Schedules the data update to run every 5 minutes.
    """
    print(f"Starting scheduled task to track coordinates for {city_to_track}. Press Ctrl+C to stop.")
    while True:
        update_and_save_data(city_to_track)
        print("Sleeping for 5 minutes...")
        time.sleep(300)

if __name__ == "__main__":
    city_to_track = "Delhi"
    run_scheduler(city_to_track)