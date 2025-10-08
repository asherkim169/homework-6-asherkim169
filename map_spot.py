import streamlit as st
import pandas as pd

st.set_page_config(page_title="Map Marking App", layout="centered")

st.title("Map Marking Generator")
st.write("Enter a latitude and longitude to visualize it on a map.")

lat = st.number_input("Enter Latitude")
lon = st.number_input("Enter Longitude")

df = pd.DataFrame({'lat': [lat], 'lon': [lon]})

st.map(df, zoom=10, use_container_width=True)

st.success(f"Map showing marker at latitude {lat} and longitude {lon}")