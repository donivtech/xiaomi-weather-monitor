from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path

app = Flask(__name__)
DATA_FILE = Path('data/weather_data.csv')

def load_data():
    """Load and process the weather data."""
    try:
        df = pd.read_csv(DATA_FILE)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def create_temperature_plot(df):
    """Create temperature visualization."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['temperature'],
        mode='lines+markers',
        name='Temperature (°C)'
    ))
    
    fig.update_layout(
        title='Temperature Over Time',
        xaxis_title='Time',
        yaxis_title='Temperature (°C)',
        template='plotly_dark'
    )
    
    return fig.to_html(full_html=False)

def create_humidity_plot(df):
    """Create humidity visualization."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['humidity'],
        mode='lines+markers',
        name='Humidity (%)'
    ))
    
    fig.update_layout(
        title='Humidity Over Time',
        xaxis_title='Time',
        yaxis_title='Humidity (%)',
        template='plotly_dark'
    )
    
    return fig.to_html(full_html=False)

def create_pressure_plot(df):
    """Create pressure visualization."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['pressure'],
        mode='lines+markers',
        name='Pressure (hPa)'
    ))
    
    fig.update_layout(
        title='Pressure Over Time',
        xaxis_title='Time',
        yaxis_title='Pressure (hPa)',
        template='plotly_dark'
    )
    
    return fig.to_html(full_html=False)

@app.route('/')
def index():
    """Render the main dashboard."""
    df = load_data()
    
    # Get latest readings
    latest = df.iloc[-1] if not df.empty else None
    
    # Create visualizations
    temp_plot = create_temperature_plot(df)
    humidity_plot = create_humidity_plot(df)
    pressure_plot = create_pressure_plot(df)
    
    return render_template('index.html',
                         latest=latest,
                         temp_plot=temp_plot,
                         humidity_plot=humidity_plot,
                         pressure_plot=pressure_plot)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 