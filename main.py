import folium as fl
from streamlit_folium import st_folium
import streamlit as st

from weather_stats import Location

st.set_page_config(
    page_title="Weather or Not",
    page_icon="images/favicon.png",
    layout="wide",
)
st.title("Weather or Not")
stats_col, map_col = st.columns([1, 3])

# Check for session state updates before overriding
if 'center' not in st.session_state:
    st.session_state["center"] = [37.7749, -122.4194]

if "zoom" not in st.session_state:
    st.session_state["zoom"] = 12

if "markers" not in st.session_state:
    st.session_state["markers"] = []

if 'info_text' not in st.session_state:
    st.session_state['info_text'] = 'Make a selection'

m = fl.Map(location=st.session_state['center'], zoom_start=st.session_state['zoom'])

with stats_col:
    st.info(st.session_state['info_text'])

# Add all existing markers to the map
for marker in st.session_state["markers"]:
    marker.add_to(m)

# Display the map only once
with map_col:
    map_data = st_folium(m)

# Handle click events
if map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lng = map_data["last_clicked"]["lng"]
    location = Location(lat=lat, lng=lng)
    location.get_hourly_stats()
    st.session_state['zoom'] = map_data['zoom']
    st.session_state['center'] = [map_data['center']['lat'], map_data['center']['lng']]
    stats_str = f"""
    🌡️    {str(round(location.temperature))}°F\n
    🌁    {str(round(location.cloud_cover))}%\n
    🍃    {str(round(location.wind_speed))}mph\n
    ☀️    {str(round(location.uv_index, 2))}
    """
    st.session_state['info_text'] = stats_str
    
    # Add the new marker to session state
    new_marker = fl.Marker(location=[lat, lng])
    if new_marker not in st.session_state["markers"]:
        st.session_state["markers"].append(new_marker)
        st.rerun()  # Rerun to update the map with the new marker