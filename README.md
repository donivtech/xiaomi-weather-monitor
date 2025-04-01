# Xiaomi Weather Monitor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python-based project that collects weather data from Xiaomi connected home devices and visualizes it on a Raspberry Pi. This project provides real-time monitoring of temperature, humidity, and air pressure data with a beautiful web interface.

## Features
- Collects temperature, humidity, and air pressure data from Xiaomi devices
- Stores data locally for historical analysis
- Real-time visualization using Plotly
- Modern, responsive web interface
- Dark mode dashboard
- Historical data tracking
- Easy setup and configuration

## Prerequisites
- Raspberry Pi (3 or 4 recommended)
- Xiaomi connected home devices (tested with Mi Temperature and Humidity Monitor 2)
- Python 3.7 or higher
- Network connectivity between devices

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/xiaomi-weather-monitor.git
cd xiaomi-weather-monitor
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your device configuration:
```bash
cp .env.example .env
```

5. Edit the `.env` file with your device details:
```
XIAOMI_DEVICE_IP=192.168.1.xxx
XIAOMI_DEVICE_TOKEN=your_device_token
```

## Getting Your Device Token

1. Use the Mi Home app to add your device
2. Use the `miio2` command-line tool to extract the token:
```bash
miio2 --ip 192.168.1.xxx --token
```
3. Or follow the [python-miio documentation](https://python-miio.readthedocs.io/en/latest/discovery.html) for token extraction

## Usage

1. Start the data collector:
```bash
python collector.py
```

2. In a separate terminal, start the visualization server:
```bash
python visualizer.py
```

3. Access the dashboard by opening a web browser and navigating to:
```
http://<raspberry-pi-ip>:5000
```

## Project Structure
```
xiaomi-weather-monitor/
├── collector.py          # Data collection script
├── visualizer.py        # Web server and visualization
├── requirements.txt     # Python dependencies
├── .env.example        # Example environment configuration
├── templates/          # HTML templates
│   └── index.html     # Main dashboard template
└── data/              # Data storage directory
    └── weather_data.csv
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [python-miio](https://github.com/rytilahti/python-miio) for Xiaomi device communication
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Plotly](https://plotly.com/) for data visualization
- [Bootstrap](https://getbootstrap.com/) for the UI framework

## Troubleshooting

- Ensure all devices are on the same network
- Check device IP and token in `.env` file
- Verify network connectivity between Raspberry Pi and Xiaomi devices
- Check the logs for any error messages
- Make sure all required ports are open and accessible 