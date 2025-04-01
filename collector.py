import os
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from miio import AirQualityMonitor
import pandas as pd

# Load environment variables
load_dotenv()

# Configuration
DEVICE_IP = os.getenv('XIAOMI_DEVICE_IP')
DEVICE_TOKEN = os.getenv('XIAOMI_DEVICE_TOKEN')
DATA_DIR = Path('data')
DATA_FILE = DATA_DIR / 'weather_data.csv'

def setup_data_directory():
    """Create data directory if it doesn't exist."""
    DATA_DIR.mkdir(exist_ok=True)
    
    # Create CSV file with headers if it doesn't exist
    if not DATA_FILE.exists():
        df = pd.DataFrame(columns=['timestamp', 'temperature', 'humidity', 'pressure', 'aqi'])
        df.to_csv(DATA_FILE, index=False)

def collect_data():
    """Collect data from Xiaomi device and save to CSV."""
    try:
        # Initialize device
        device = AirQualityMonitor(DEVICE_IP, DEVICE_TOKEN)
        
        # Get sensor data
        data = device.status()
        
        # Create data record
        record = {
            'timestamp': datetime.now().isoformat(),
            'temperature': data.temperature,
            'humidity': data.humidity,
            'pressure': data.pressure,
            'aqi': data.aqi
        }
        
        # Append to CSV
        df = pd.DataFrame([record])
        df.to_csv(DATA_FILE, mode='a', header=False, index=False)
        
        print(f"Data collected: {record}")
        return record
        
    except Exception as e:
        print(f"Error collecting data: {e}")
        return None

def main():
    """Main function to continuously collect data."""
    print("Starting Xiaomi Weather Monitor...")
    setup_data_directory()
    
    while True:
        collect_data()
        time.sleep(300)  # Collect data every 5 minutes

if __name__ == "__main__":
    main() 