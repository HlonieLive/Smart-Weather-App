# Real-time weather data fetching using Open-Meteo API

import requests
import json
from datetime import datetime

def get_coordinates(city_name):
    """Fetch coordinates for a given city name using Open-Meteo Geocoding API."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "name": result["name"],
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "country": result.get("country", ""),
                "timezone": result.get("timezone", "UTC")
            }
    return None

def get_weather(lat, lon):
    """Fetch real-time weather data for given coordinates."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_weather_description(temp):
    """Return a descriptive state based on temperature."""
    if temp < 0:
        return "Freezing Cold"
    elif 0 <= temp < 10:
        return "Cold"
    elif 10 <= temp < 20:
        return "Cool"
    elif 20 <= temp < 30:
        return "Warm"
    else:
        return "Hot"

def get_clothing_suggestion(temp):
    """Return a clothing suggestion based on temperature."""
    if temp < 0:
        return "Wear heavy winter jacket, scarf, gloves, and hat."
    elif 0 <= temp < 10:
        return "Wear a coat or a thick sweater."
    elif 10 <= temp < 20:
        return "A light jacket or sweater is recommended."
    elif 20 <= temp < 30:
        return "T-shirt and light pants/shorts are fine."
    else:
        return "Wear light, breathable clothing. Stay hydrated."

def main():
    print("--- Smart Weather App Backend Verification ---")
    while True:
        print("\nPress 'q' to quit.")
        city = input("Enter city name: ").capitalize()
        if city.lower() == 'q':
            break
    
        print(f"\nSearching for {city}...")
        location = get_coordinates(city)
    
        if location:
            print(f"Found: {location['name']}, {location['country']} ({location['latitude']}, {location['longitude']})")
            weather = get_weather(location['latitude'], location['longitude'])
        
            if weather:
                current = weather['current']
                appt_temp = current['apparent_temperature']
                weather_desc = get_weather_description(appt_temp)
                clothing_suggestion = get_clothing_suggestion(appt_temp)

                print("\n--- Current Weather ---")
                print(f"Timezone: {location['timezone']}")
                print(f"Date: {datetime.now().strftime('%A, %d %b %Y')}")
                print(f"Temperature: {current['temperature_2m']}°C")
                print(f"Apparent Temp: {appt_temp}°C")
                print(f"Humidity: {current['relative_humidity_2m']}%")
                print(f"Wind Speed: {current['wind_speed_10m']} km/h")
                print(f"Condition Code: {current['weather_code']}")
                print(f"\nWeather Description:\nIt is {weather_desc} today.\n{clothing_suggestion}")
            else:
                print("Failed to fetch weather data.")
        else:
            print("City not found. Try again...")

if __name__ == "__main__":
    main()