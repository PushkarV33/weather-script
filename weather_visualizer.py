import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timezone
import json

# Set Seaborn style for better visuals
sns.set_style("darkgrid")

# API setup (replace with your API key)
API_KEY = "Your_API_Key_Here"  # Get from openweathermap.org[2]
LAT = "51.5074"  # Latitude for London
LON = "-0.1278"  # Longitude for London
URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&exclude=minutely,daily,alerts&units=metric&appid={API_KEY}"


def fetch_weather_data():
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Raise error for bad status codes
        data = response.json()

        # Extract current weather
        current = data['current']
        current_temp = current['temp']
        current_humidity = current['humidity']
        current_weather = current['weather'][0]['description']

        # Extract hourly forecast (next 24 hours for simplicity)
        hourly = data['hourly'][:24]
        hours = [datetime.fromtimestamp(
            h['dt'], tz=timezone.utc).strftime('%H:%M') for h in hourly]
        temps = [h['temp'] for h in hourly]
        humidities = [h['humidity'] for h in hourly]

        return {
            'current_temp': current_temp,
            'current_humidity': current_humidity,
            'current_weather': current_weather,
            'hours': hours,
            'temps': temps,
            'humidities': humidities
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def create_visualizations(data):
    if not data:
        return

    # Plot 1: Hourly Temperature Forecast
    plt.figure(figsize=(10, 5))
    plt.plot(data['hours'], data['temps'],
             marker='o', linestyle='-', color='b')
    plt.title('Hourly Temperature Forecast')
    plt.xlabel('Time (UTC)')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('temperature_forecast.png')
    plt.show()

    # Plot 2: Hourly Humidity Forecast
    plt.figure(figsize=(10, 5))
    plt.plot(data['hours'], data['humidities'],
             marker='o', linestyle='-', color='g')
    plt.title('Hourly Humidity Forecast')
    plt.xlabel('Time (UTC)')
    plt.ylabel('Humidity (%)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('humidity_forecast.png')
    plt.show()


# Main execution
if __name__ == "__main__":
    weather_data = fetch_weather_data()
    if weather_data:
        print(f"Current Temperature: {weather_data['current_temp']}°C[7]")
        print(f"Current Humidity: {weather_data['current_humidity']}%[7]")
        print(f"Current Weather: {weather_data['current_weather']}[7]")
        create_visualizations(weather_data)
