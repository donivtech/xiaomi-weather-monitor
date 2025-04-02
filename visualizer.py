from flask import Flask, render_template
import pandas as pd
from pathlib import Path
import json

app = Flask(__name__)

# Configuration
DATA_DIR = Path('data')
DATA_FILE = DATA_DIR / 'weather_data.csv'

def load_data():
    """Load data from CSV file."""
    try:
        df = pd.read_csv('data/weather_data.csv')
        print(f"\nData loaded successfully:")
        print(f"Number of rows: {len(df)}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"Data range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        print("\nSample data:")
        print(df.head())
        print("\nData types:")
        print(df.dtypes)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def prepare_chart_data(df):
    """Prepare data for charts."""
    try:
        # Create a copy of the dataframe first
        df = df.copy()
        
        # Get last 24 readings
        df = df.tail(24).reset_index(drop=True)
        print(f"\nPreparing chart data:")
        print(f"Number of data points: {len(df)}")
        
        # Convert timestamps to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Format timestamps for display
        df['time'] = df['timestamp'].dt.strftime('%H:%M')
        
        # If there are duplicate timestamps, keep the last value for each timestamp
        df = df.drop_duplicates(subset=['time'], keep='last')
        
        print("\nTemperature data:")
        print(df[['time', 'temperature']].head())
        print("\nHumidity data:")
        print(df[['time', 'humidity']].head())
        
        # Prepare data for charts - using simple arrays
        chart_data = {
            'labels': df['time'].tolist(),
            'temperature': df['temperature'].tolist(),
            'humidity': df['humidity'].tolist()
        }
        
        print("\nFinal chart data:")
        print(f"Number of labels: {len(chart_data['labels'])}")
        print(f"Sample labels: {chart_data['labels'][:5]}")
        print(f"Sample temperature: {chart_data['temperature'][:5]}")
        print(f"Sample humidity: {chart_data['humidity'][:5]}")
        
        return chart_data
    except Exception as e:
        print(f"Error preparing chart data: {e}")
        return {'labels': [], 'temperature': [], 'humidity': []}

@app.route('/')
def index():
    """Display weather data dashboard."""
    df = load_data()
    
    if df.empty:
        print("No data available")
        return render_template('index.html',
                             latest=None,
                             temperature_data=[],
                             humidity_data=[],
                             chart_data={'labels': [], 'temperature': [], 'humidity': []},
                             has_data=False)
    
    # Get latest readings
    latest = df.iloc[-1].to_dict()
    print(f"Latest reading: {latest}")
    
    # Prepare data for charts
    chart_data = prepare_chart_data(df)
    
    return render_template('index.html',
                         latest=latest,
                         temperature_data=json.dumps(chart_data['temperature']),
                         humidity_data=json.dumps(chart_data['humidity']),
                         chart_data=chart_data,
                         has_data=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 