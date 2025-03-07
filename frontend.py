import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

# Configuration
CITIES = ["Delhi", "New York", "London", "Tokyo"]
CITY_COLORS = {
    "Delhi": "#FF5733",
    "New York": "#33A1FF",
    "London": "#33FF57",
    "Tokyo": "#D033FF"
}

# Initialize data structures
@st.cache_resource
def get_data_store():
    return {
        "temperatures": {city: [] for city in CITIES},
        "humidity": {city: [] for city in CITIES},
        "pressure": {city: [] for city in CITIES},
        "wind_speed": {city: [] for city in CITIES},
        "timestamps": [],
        "weather_conditions": {city: [] for city in CITIES},
    }

data_store = get_data_store()

# Set up Streamlit page
st.set_page_config(
    page_title="Weather Data Comparison",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("🌦️ Global Weather Dashboard")
st.markdown("Real-time weather monitoring across major global cities")

# Initialize session states
if 'is_streaming' not in st.session_state:
    st.session_state.is_streaming = False

if 'simulated_data' not in st.session_state:
    st.session_state.simulated_data = False

# Sidebar for controls
with st.sidebar:
    st.header("Dashboard Controls")
    
    # Button to simulate data (instead of using Kafka)
    if not st.session_state.is_streaming:
        if st.button("Start Weather Simulation", key="start_stream"):
            st.session_state.is_streaming = True
            st.session_state.simulated_data = True
            st.rerun()
    else:
        st.success("Weather data simulation is active!")
        
        if st.button("Stop Weather Simulation", key="stop_stream"):
            st.session_state.is_streaming = False
            st.rerun()
    
    st.markdown("---")
    
    update_interval = st.slider(
        "Update Interval (seconds)",
        min_value=1,
        max_value=10,
        value=2
    )
    
    max_data_points = st.slider(
        "Data History Length",
        min_value=10,
        max_value=50,
        value=20
    )
    
    temp_unit = st.radio(
        "Temperature Unit",
        options=["Celsius", "Fahrenheit"],
        index=0
    )
    
    selected_cities = st.multiselect(
        "Cities to Display",
        options=CITIES,
        default=CITIES
    )
    
    visualization_type = st.selectbox(
        "Chart Type",
        options=["Line Chart", "Bar Chart", "Area Chart"],
        index=0
    )

# Function to convert temperature if needed
def convert_temp(temp_c):
    if temp_unit == "Fahrenheit":
        return (temp_c * 9/5) + 32
    return temp_c

# Function to format timestamp
def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

# Function to generate simulated weather data
def generate_simulated_data():
    import random
    import time
    
    current_time = time.time()
    data_store["timestamps"].append(current_time)
    
    for city in CITIES:
        # Generate random but realistic weather data
        if not data_store["temperatures"][city]:
            # Initialize with baseline values for each city
            if city == "Delhi":
                temp_base = 28
            elif city == "New York":
                temp_base = 15
            elif city == "London":
                temp_base = 12
            else:  # Tokyo
                temp_base = 20
                
            # Add some randomness
            temp = temp_base + random.uniform(-2, 2)
            humidity = random.uniform(40, 80)
            pressure = random.uniform(1000, 1025)
            wind_speed = random.uniform(1, 8)
            
            # Set conditions based on temperature and humidity
            if temp > 25 and humidity < 50:
                weather_condition = "Clear"
            elif temp > 20 and humidity > 70:
                weather_condition = "Rain"
            elif temp < 10:
                weather_condition = "Cold"
            else:
                weather_condition = "Clouds"
        else:
            # Base values on previous readings with small changes
            last_temp = data_store["temperatures"][city][-1]
            last_humidity = data_store["humidity"][city][-1]
            last_pressure = data_store["pressure"][city][-1]
            last_wind = data_store["wind_speed"][city][-1]
            
            # Small random changes
            temp = last_temp + random.uniform(-0.5, 0.5)
            humidity = max(min(last_humidity + random.uniform(-3, 3), 100), 0)
            pressure = last_pressure + random.uniform(-1, 1)
            wind_speed = max(last_wind + random.uniform(-0.5, 0.5), 0)
            
            # Determine weather condition based on current values
            if temp > 25 and humidity < 50:
                weather_condition = "Clear"
            elif temp > 20 and humidity > 70:
                weather_condition = "Rain"
            elif temp < 10:
                weather_condition = "Cold"
            else:
                weather_condition = "Clouds"
        
        # Store the data
        data_store["temperatures"][city].append(temp)
        data_store["humidity"][city].append(humidity)
        data_store["pressure"][city].append(pressure)
        data_store["wind_speed"][city].append(wind_speed)
        data_store["weather_conditions"][city].append(weather_condition)
        
        # Keep only the latest max_data_points
        if len(data_store["temperatures"][city]) > max_data_points:
            data_store["temperatures"][city].pop(0)
            data_store["humidity"][city].pop(0)
            data_store["pressure"][city].pop(0)
            data_store["wind_speed"][city].pop(0)
            data_store["weather_conditions"][city].pop(0)
    
    # Keep timestamps consistent with data points
    if len(data_store["timestamps"]) > max_data_points:
        data_store["timestamps"].pop(0)
    
    return True

# Function to create the main temperature chart
def create_temperature_chart(selected_cities):
    if not data_store["timestamps"] or not any(data_store["temperatures"][city] for city in selected_cities):
        return go.Figure().update_layout(title="Waiting for data...")
    
    fig = go.Figure()
    
    for city in selected_cities:
        if len(data_store["temperatures"][city]) > 0:
            # Get timestamps and temperatures for the city
            timestamps = data_store["timestamps"][-len(data_store["temperatures"][city]):]
            temps = [convert_temp(t) for t in data_store["temperatures"][city]]
            
            if visualization_type == "Line Chart":
                fig.add_trace(go.Scatter(
                    x=[format_timestamp(ts) for ts in timestamps],
                    y=temps,
                    mode='lines+markers',
                    name=city,
                    line=dict(color=CITY_COLORS[city], width=2),
                    marker=dict(size=6),
                ))
            elif visualization_type == "Bar Chart":
                fig.add_trace(go.Bar(
                    x=[format_timestamp(ts) for ts in timestamps],
                    y=temps,
                    name=city,
                    marker_color=CITY_COLORS[city],
                ))
            elif visualization_type == "Area Chart":
                fig.add_trace(go.Scatter(
                    x=[format_timestamp(ts) for ts in timestamps],
                    y=temps,
                    name=city,
                    fill='tozeroy',
                    line=dict(color=CITY_COLORS[city], width=2),
                ))
    
    unit_suffix = "°F" if temp_unit == "Fahrenheit" else "°C"
    
    fig.update_layout(
        title=f"Temperature Comparison ({temp_unit})",
        xaxis_title="Time",
        yaxis_title=f"Temperature ({unit_suffix})",
        height=400,
        legend=dict(orientation="h", y=1.02, x=1, xanchor="right"),
        hovermode="x unified",
        margin=dict(l=20, r=20, t=60, b=40),
        plot_bgcolor="#f9f9f9",
    )
    
    return fig

# Function to create a humidity comparison chart
def create_humidity_chart(selected_cities):
    if not data_store["timestamps"] or not any(data_store["humidity"][city] for city in selected_cities):
        return go.Figure().update_layout(title="Waiting for data...")
    
    fig = go.Figure()
    
    for city in selected_cities:
        if len(data_store["humidity"][city]) > 0:
            fig.add_trace(go.Scatter(
                x=[format_timestamp(ts) for ts in data_store["timestamps"][-len(data_store["humidity"][city]):]], 
                y=data_store["humidity"][city],
                mode='lines',
                name=city,
                line=dict(color=CITY_COLORS[city], width=2),
            ))
    
    fig.update_layout(
        title="Humidity Comparison (%)",
        xaxis_title="Time",
        yaxis_title="Humidity (%)",
        height=300,
        margin=dict(l=20, r=20, t=40, b=40),
        plot_bgcolor="#f9f9f9",
    )
    
    return fig

# Function to create wind speed comparison
def create_wind_chart(selected_cities):
    if not any(data_store["wind_speed"][city] for city in selected_cities):
        return go.Figure().update_layout(title="Waiting for data...")
    
    fig = go.Figure()
    
    for city in selected_cities:
        if len(data_store["wind_speed"][city]) > 0:
            fig.add_trace(go.Bar(
                x=[city],
                y=[data_store["wind_speed"][city][-1]],
                name=city,
                marker_color=CITY_COLORS[city],
                text=[f"{data_store['wind_speed'][city][-1]:.1f} m/s"],
                textposition='auto',
            ))
    
    fig.update_layout(
        title="Current Wind Speed (m/s)",
        xaxis_title="City",
        yaxis_title="Wind Speed (m/s)",
        height=300,
        margin=dict(l=20, r=20, t=40, b=40),
        plot_bgcolor="#f9f9f9",
    )
    
    return fig

# Function to create city metrics cards
def city_metrics_cards(selected_cities):
    cols = st.columns(len(selected_cities))
    
    for i, city in enumerate(selected_cities):
        with cols[i]:
            st.markdown(f"### {city}")
            
            if (data_store["temperatures"].get(city) and len(data_store["temperatures"][city]) > 0):
                temp = convert_temp(data_store["temperatures"][city][-1])
                unit_suffix = "°F" if temp_unit == "Fahrenheit" else "°C"
                humidity = data_store["humidity"][city][-1] if data_store["humidity"][city] else "N/A"
                wind = data_store["wind_speed"][city][-1] if data_store["wind_speed"][city] else "N/A"
                condition = data_store["weather_conditions"][city][-1] if data_store["weather_conditions"][city] else "Unknown"
                
                # Determine weather emoji
                weather_emoji = "🌦️"  # default
                if condition.lower() == "clear":
                    weather_emoji = "☀️"
                elif condition.lower() == "clouds":
                    weather_emoji = "☁️"
                elif condition.lower() == "rain":
                    weather_emoji = "🌧️"
                elif condition.lower() == "cold":
                    weather_emoji = "❄️"
                
                col1, col2 = st.columns([2, 1])
                col1.metric("Temperature", f"{temp:.1f}{unit_suffix}")
                col2.markdown(f"<h1 style='text-align: center;'>{weather_emoji}</h1>", unsafe_allow_html=True)
                
                st.metric("Humidity", f"{humidity:.1f}%")
                st.metric("Wind Speed", f"{wind:.1f} m/s")
                st.caption(f"Condition: {condition}")
            else:
                st.info("Waiting for data...")

# Main app execution
if st.session_state.is_streaming:
    # Create layout containers
    metrics_container = st.container()
    main_chart_container = st.container()
    secondary_charts = st.container()
    
    # Generate simulated data if in simulation mode
    if st.session_state.simulated_data:
        generate_simulated_data()
    
    # Display city metrics at the top
    with metrics_container:
        city_metrics_cards(selected_cities)
    
    # Main temperature chart
    with main_chart_container:
        st.plotly_chart(create_temperature_chart(selected_cities), use_container_width=True)
    
    # Secondary charts in a grid
    with secondary_charts:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_humidity_chart(selected_cities), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_wind_chart(selected_cities), use_container_width=True)
    
    # Set up automatic refresh
    time.sleep(update_interval)
    st.rerun()
else:
    # Display a message when not streaming
    st.info("Click the 'Start Weather Simulation' button in the sidebar to begin viewing weather data.")