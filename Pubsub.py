import os
import requests
from datetime import datetime
import json

today = datetime.now().strftime('%Y-%m-%d')
folder_name = f"vehicle_data_{today}"

os.makedirs(folder_name, exist_ok=True)


vehicle_ids = ['3319', '3419']
all_data = []  # List to store all breadcrumb data


for vehicle_id in vehicle_ids:
    url = f"https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id={vehicle_id}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        vehicle_data = response.json()
        all_data.extend(vehicle_data)

        print(f"Successfully downloaded data for vehicle ID: {vehicle_id}")

    except requests.RequestException as e:
        print(f"An error occurred for vehicle ID {vehicle_id}: {e}")

# Save all fetched data into a single file
with open('bcsample.json', 'w') as f:
    json.dump(all_data, f, indent=4)

print("All data saved to bcsample.json")