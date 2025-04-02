import os
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from miio import Device

# Load environment variables
load_dotenv()

# Configuration
DEVICE_IP = os.getenv('XIAOMI_DEVICE_IP')
DEVICE_TOKEN = os.getenv('XIAOMI_DEVICE_TOKEN')
DATA_DIR = Path('data')
DATA_FILE = DATA_DIR / 'weather_data.csv'

def get_device_info(device):
    """Get device information."""
    try:
        info = device.info()
        print(f"Device info: Model: {info.model}")
        print(f"Hardware version: {info.hardware_version}")
        print(f"Firmware version: {info.firmware_version}")
        return True
    except Exception as e:
        print(f"Error getting device info: {e}")
        return False

def get_device_status(device):
    """Get device status using miio library."""
    try:
        status = []
        
        # Get temperature
        try:
            temp_result = device.send("get_properties", [{"siid": 3, "piid": 7}])
            if temp_result and len(temp_result) > 0 and temp_result[0].get('code') == 0:
                # Temperature is already in °C
                temp_value = temp_result[0].get('value')
                status.append({'did': 'temperature', 'value': temp_value})
                print(f"Successfully got temperature: {temp_value}°C")
            else:
                print(f"Invalid temperature response: {temp_result}")
        except Exception as e:
            print(f"Error getting temperature: {e}")
        
        # Get humidity
        try:
            humid_result = device.send("get_properties", [{"siid": 3, "piid": 8}])
            if humid_result and len(humid_result) > 0 and humid_result[0].get('code') == 0:
                # Humidity needs to be scaled by 1.6
                raw_humid = humid_result[0].get('value')
                humid_value = round(raw_humid / 1.6, 1)
                status.append({'did': 'humidity', 'value': humid_value})
                print(f"Successfully got humidity: {humid_value}% (raw: {raw_humid})")
            else:
                print(f"Invalid humidity response: {humid_result}")
        except Exception as e:
            print(f"Error getting humidity: {e}")
        
        if status:
            return status
        
        print("No valid data received")
        return None
            
    except Exception as e:
        print(f"Error getting device status: {e}")
        return None

def setup_data_directory():
    """Create data directory if it doesn't exist."""
    DATA_DIR.mkdir(exist_ok=True)
    
    # Create CSV file with headers if it doesn't exist
    if not DATA_FILE.exists():
        df = pd.DataFrame(columns=['timestamp', 'temperature', 'humidity', 'mode', 'target_humidity'])
        df.to_csv(DATA_FILE, index=False)

def collect_data(device):
    """Collect data from Xiaomi device and save to CSV."""
    try:
        # Get device info first
        if not get_device_info(device):
            print("Failed to get device info")
            return None

        # Get device status
        status = get_device_status(device)
        if not status:
            print("Failed to get device status")
            return None

        print(f"Received status: {status}")
        
        # Parse the response
        data = {}
        for prop in status:
            if prop['did'] == 'temperature':
                data['temperature'] = prop['value']
            elif prop['did'] == 'humidity':
                data['humidity'] = prop['value']
        
        # Create data record
        record = {
            'timestamp': datetime.now().isoformat(),
            'temperature': data.get('temperature', 0),
            'humidity': data.get('humidity', 0),
            'mode': 'Unknown',  # Default value since we're not collecting it
            'target_humidity': 0  # Default value since we're not collecting it
        }
        
        # Append to CSV
        df = pd.DataFrame([record])
        df.to_csv(DATA_FILE, mode='a', header=False, index=False)
        
        print(f"Data collected: {record}")
        return record
        
    except Exception as e:
        print(f"Error collecting data: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return None

def main():
    """Main function to continuously collect data."""
    print("Starting Xiaomi Weather Monitor...")
    print(f"Device IP: {DEVICE_IP}")
    print(f"Token length: {len(DEVICE_TOKEN)}")
    setup_data_directory()
    
    # Create device instance
    device = Device(DEVICE_IP, DEVICE_TOKEN)
    
    while True:
        collect_data(device)
        time.sleep(300)  # Collect data every 5 minutes

if __name__ == "__main__":
    main() 