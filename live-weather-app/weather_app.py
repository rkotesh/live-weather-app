import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="🌤 Live Weather App", layout="centered")
st.title("🌤 Live Weather App")
st.markdown("Enter a city name below to get real-time weather updates.")

# ---- Function to Get Weather ----
def fetch_weather(city_name):
    try:
        params = {
            "q": city_name,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}

# ---- User Input ----
city = st.text_input("Enter City Name", placeholder="e.g. Guntur, Delhi, New York")

# ---- Fetch Weather on Button Click ----
if st.button("Get Weather"):
    if not city:
        st.warning("Please enter a city name.")
    else:
        with st.spinner("Fetching weather..."):
            data = fetch_weather(city)

            if data.get("cod") == 200:
                # Display Weather Info
                st.success(f"Weather in {data['name']}, {data['sys']['country']}")
                st.metric(label="🌡 Temperature", value=f"{data['main']['temp']} °C")
                st.write(f"**☁ Condition:** {data['weather'][0]['description'].title()}")
                st.write(f"**💧 Humidity:** {data['main']['humidity']}%")
                st.write(f"**🌬 Wind Speed:** {data['wind']['speed']} m/s")
            elif data.get("message"):
                st.error(f"❌ {data.get('message').capitalize()}")
            else:
                st.error("Something went wrong. Please try again.")

# ---- Footer ----
st.markdown("---")

