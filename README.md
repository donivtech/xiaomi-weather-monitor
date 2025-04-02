# Xiaomi Weather Monitor

A Python application to collect and visualize temperature and humidity data from a Xiaomi humidifier (model: zhimi.humidifier.ca4).

## Features

- Real-time data collection from Xiaomi humidifier
- Web-based dashboard showing:
  - Current temperature and humidity
  - 24-hour history charts
  - Dark theme for better visibility

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd xiaomi_weather_monitor
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your device:
   - Find your device's IP address (e.g., using your router's interface)
   - Get your device token (using Mi Home app or miio tools)
   - Update the IP and token in the collector script

## Usage

1. Start the data collector:
```bash
python collector.py
```

2. Start the visualization server:
```bash
python visualizer.py
```

3. Open your web browser and navigate to:
   - http://localhost:5000 (local access)
   - http://<your-ip>:5000 (network access)

## Data Storage

- Data is stored in CSV format in `data/weather_data.csv`
- Fields include: timestamp, temperature, humidity, mode, target_humidity
- Temperature is in °C
- Humidity is in % (scaled appropriately)

## Requirements

- Python 3.8 or higher
- Network access to your Xiaomi device
- Dependencies listed in requirements.txt 