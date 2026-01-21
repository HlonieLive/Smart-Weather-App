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

def get_weather_condition(code):
    """Return a string description of the weather code (WMO)."""
    if code == 0: return "Clear Sky"
    if code in [1, 2, 3]: return "Partly Cloudy"
    if code in [45, 48]: return "Foggy"
    if code in [51, 53, 55]: return "Drizzling"
    if code in [56, 57]: return "Freezing Drizzle"
    if code in [61, 63, 65]: return "Raining"
    if code in [66, 67]: return "Freezing Rain"
    if code in [71, 73, 75]: return "Snowing"
    if code == 77: return "Snow Grains"
    if code in [80, 81, 82]: return "Rain Showers"
    if code in [85, 86]: return "Snow Showers"
    if code == 95: return "Thunderstorm"
    if code in [96, 99]: return "Thunderstorm with Hail"
    return "Unknown Condition"

def get_clothing_suggestion(temp, code=None):
    """Return a clothing suggestion based on temperature and weather condition."""
    suggestion = ""
    
    # Temperature-based suggestions
    if temp < 0:
        suggestion = "Wear heavy winter jacket, scarf, gloves, and hat."
    elif 0 <= temp < 10:
        suggestion = "Wear a coat or a thick sweater."
    elif 10 <= temp < 20:
        suggestion = "A light jacket or sweater is recommended."
    elif 20 <= temp < 30:
        suggestion = "T-shirt and light pants/shorts are fine."
    else:
        suggestion = "Wear light, breathable clothing. Stay hydrated."

    # Weather condition-based additions
    if code is not None:
        # Rain/Drizzle/Thunderstorm
        if code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99]:
            suggestion += " Don't forget an umbrella or raincoat!"
        # Snow
        elif code in [71, 73, 75, 77, 85, 86]:
            suggestion += " Wear waterproof boots."

    return suggestion

def main():
    print("--- Smart Weather App ---")
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
                w_code = current['weather_code']
                
                weather_desc = get_weather_description(appt_temp)
                condition_desc = get_weather_condition(w_code)
                clothing_suggestion = get_clothing_suggestion(appt_temp, w_code)

                print(f"Timezone: {location['timezone']}")
                print(f"Date: {datetime.now().strftime('%A, %d %b %Y')}\n")

                print("\n--- Current Weather ---")
                print(f"Temperature: {current['temperature_2m']}°C")
                print(f"Apparent Temp: {appt_temp}°C")
                print(f"Humidity: {current['relative_humidity_2m']}%")
                print(f"Wind Speed: {current['wind_speed_10m']} km/h")
                print(f"Condition: {condition_desc}")
                print(f"\nWeather Description:\nIt is {condition_desc} and {weather_desc} today.\n{clothing_suggestion}")
            else:
                print("Failed to fetch weather data.")
        else:
            print("City not found. Try again...")

if __name__ == "__main__":
    main()