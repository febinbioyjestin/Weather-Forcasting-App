import pyowm
import streamlit as st
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pytz


# Set page configuration
st.set_page_config(
    page_title="Weather Forecast",
    page_icon=":partly_sunny:",
    # layout="wide"
)

# Initialize OpenWeatherMap API
owm = pyowm.OWM(API-KEY)
mgr = owm.weather_manager()

# Function to plot bar chart
def plot_bar_chart(days, temp_min, temp_max):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(days, temp_min, label='Min Temperature', color='skyblue', alpha=0.5)
    ax.bar(days, temp_max, label='Max Temperature', color='salmon', alpha=0.5)
    ax.set_xlabel('Days')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Weather Forecast')
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Function to plot line chart
def plot_line_chart(days, temp_min, temp_max):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(days, temp_min, marker='o', label='Min Temperature', color='skyblue')
    ax.plot(days, temp_max, marker='o', label='Max Temperature', color='salmon')
    ax.set_xlabel('Days')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Weather Forecast')
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Streamlit frontend setup
# st.title("Weather Forecast")
st.markdown("<h1 style='text-align: center;'>Weather Forecast</h1>", unsafe_allow_html=True)
st.markdown("---")
st.write("### Write the name of a City (hit the enter) and select the Temperature Unit and Graph Type...")

# Input city name
place = st.text_input("NAME OF THE CITY :", "")

# Select temperature unit
unit = st.selectbox("Select Temperature Unit", ("Celsius", "Fahrenheit"))

# Select graph type
g_type = st.selectbox("Select Graph Type", ("Line Graph", "Bar Graph"))

submit_btn = st.button("Submit")

if submit_btn:
    if place == "":
        st.warning("Please input a city name.")
    else:
        # Fetch weather forecast data
        try:
            forecaster = mgr.forecast_at_place(place, '3h')
            forecast = forecaster.forecast
            st.write(f"Weather forecast for {place}")

            # Extract forecast data
            days = []
            temp_min = []
            temp_max = []
            for weather in forecast:
                day = datetime.utcfromtimestamp(weather.reference_time()).strftime('%Y-%m-%d')
                if day not in days:
                    days.append(day)
                    temp_min.append(weather.temperature(unit='celsius')['temp_min'])
                    temp_max.append(weather.temperature(unit='celsius')['temp_max'])

            # Plot temperature
            if g_type == "Line Graph":
                plot_line_chart(days, temp_min, temp_max)
            else:
                plot_bar_chart(days, temp_min, temp_max)

            # Additional weather updates
            st.write("#### Additional Weather Updates:")
            st.write("- 🌧️ Impending Rain:", "Yes" if forecaster.will_have_rain() else "No")
            st.write("- ☀️ Clear Sky:", "Yes" if forecaster.will_have_clear() else "No")
            st.write("- 🌫️ Fog:", "Yes" if forecaster.will_have_fog() else "No")
            st.write("- ☁️ Clouds:", "Yes" if forecaster.will_have_clouds() else "No")
            st.write("- ❄️ Snow:", "Yes" if forecaster.will_have_snow() else "No")
            st.write("- ⛈️ Storm:", "Yes" if forecaster.will_have_storm() else "No")
            st.write("- 🌪️ Tornado:", "Yes" if forecaster.will_have_tornado() else "No")
            st.write("- 🌀 Hurricane:", "Yes" if forecaster.will_have_hurricane() else "No")

            # sunrise and sunset times
            observation = mgr.weather_at_place(place)
            fweather = observation.weather
            sunrise_iso = fweather.sunrise_time(timeformat='iso')
            sunrset_iso = fweather.sunset_time(timeformat='iso')
            # Display sunrise and sunset times
            st.write("#### Sunrise and Sunset Times:")
            st.write(f"- Sunrise Time (GMT): {sunrise_iso}")
            st.write(f"- Sunset Time (GMT): {sunrset_iso}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.error("Please make sure you have entered a valid city name.")


# Sidebar
st.sidebar.title("About Me")
st.sidebar.markdown("---")

# Add your photo
st.sidebar.image("profile-pic (2).png", width=150)

# Add your name
st.sidebar.title("Hemant Kumar")

# Define your social media profile links
linkedin_link = "https://www.linkedin.com/in/hemantkumar421"
github_link = "https://github.com/MrJi421"
instagram_link = "https://www.instagram.com/mr.ji421"
email_link = "mailto:mr.ji421@outlook.com"
# Add Font Awesome CSS link
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">', unsafe_allow_html=True)

# Define the icons for each social media platform
linkedin_icon = '<i class="fab fa-linkedin"></i>'
github_icon = '<i class="fab fa-github"></i>'
instagram_icon = '<i class="fab fa-instagram"></i>'
email_icon = '<i class="fas fa-envelope"></i>'

# Add links to the sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("Contact me")
st.sidebar.markdown(f"[{linkedin_icon}]({linkedin_link})", unsafe_allow_html=True)
st.sidebar.markdown(f"[{github_icon}]({github_link})", unsafe_allow_html=True)
st.sidebar.markdown(f"[{instagram_icon}]({instagram_link})", unsafe_allow_html=True)
st.sidebar.markdown(f"[{email_icon}]({email_link})", unsafe_allow_html=True)
