# Real-time weather data fetching using Open-Meteo API

import requests
import json

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

def main():
    print("--- Smart Weather App Backend Verification ---")
    city = input("Enter city name: ") or "London"
    
    print(f"\nSearching for {city}...")
    location = get_coordinates(city)
    
    if location:
        print(f"Found: {location['name']}, {location['country']} ({location['latitude']}, {location['longitude']})")
        weather = get_weather(location['latitude'], location['longitude'])
        
        if weather:
            current = weather['current']
            print("\n--- Current Weather ---")
            print(f"Temperature: {current['temperature_2m']}°C")
            print(f"Apparent Temp: {current['apparent_temperature']}°C")
            print(f"Humidity: {current['relative_humidity_2m']}%")
            print(f"Wind Speed: {current['wind_speed_10m']} km/h")
            print(f"Condition Code: {current['weather_code']}")
        else:
            print("Failed to fetch weather data.")
    else:
        print("City not found.")

if __name__ == "__main__":
    main()