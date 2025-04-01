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
        name='Current Humidity (%)'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['target_humidity'],
        mode='lines+markers',
        name='Target Humidity (%)'
    ))
    
    fig.update_layout(
        title='Humidity Over Time',
        xaxis_title='Time',
        yaxis_title='Humidity (%)',
        template='plotly_dark'
    )
    
    return fig.to_html(full_html=False)

def create_mode_plot(df):
    """Create mode visualization."""
    fig = go.Figure()
    
    # Count modes over time
    mode_counts = df.groupby(['timestamp', 'mode']).size().unstack(fill_value=0)
    
    for mode in mode_counts.columns:
        fig.add_trace(go.Scatter(
            x=mode_counts.index,
            y=mode_counts[mode],
            mode='lines+markers',
            name=mode
        ))
    
    fig.update_layout(
        title='Device Mode Over Time',
        xaxis_title='Time',
        yaxis_title='Count',
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
    mode_plot = create_mode_plot(df)
    
    return render_template('index.html',
                         latest=latest,
                         temp_plot=temp_plot,
                         humidity_plot=humidity_plot,
                         mode_plot=mode_plot)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 