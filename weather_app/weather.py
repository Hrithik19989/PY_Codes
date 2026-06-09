import requests
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL  = "https://api.openweathermap.org/data/2.5"
FAVS_FILE = Path("favourites.json")
UNITS     = "metric"                # metric = Celsius, imperial = Fahrenheit

def get_weather(city):
    url    = f"{BASE_URL}/weather"
    params = {"q": city, "appid": API_KEY, "units": UNITS}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"  City '{city}' not found.")
        else:
            print(f"  API error: {e}")
    except requests.exceptions.ConnectionError:
        print("  No internet connection.")
    except requests.exceptions.Timeout:
        print("  Request timed out.")
    return None

WIND_DIR = ["N","NE","E","SE","S","SW","W","NW"]

def wind_direction(degrees):
    index = round(degrees / 45) % 8
    return WIND_DIR[index]

def display_weather(data):
    city      = data["name"]
    country   = data["sys"]["country"]
    temp      = data["main"]["temp"]
    feels     = data["main"]["feels_like"]
    humidity  = data["main"]["humidity"]
    condition = data["weather"][0]["description"].title()
    wind_spd  = data["wind"]["speed"]
    wind_deg  = data["wind"].get("deg", 0)
    visibility = data.get("visibility", 0) // 1000   # convert m to km

    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
    sunset  = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

    print(f"""
  ╔══════════════════════════════════════╗
  ║  {city}, {country:<34}║
  ╠══════════════════════════════════════╣
  ║  🌡  Temp      : {temp:>5.1f}°C ({feels:.1f}°C feels)  ║
  ║  💧 Humidity  : {humidity:>5}%                   ║
  ║  🌬  Wind      : {wind_spd:>4.1f} m/s {wind_direction(wind_deg):<3}           ║
  ║  👁  Visibility: {visibility:>4} km                  ║
  ║  ☁  Condition : {condition:<22}║
  ║  🌅 Sunrise   : {sunrise}                     ║
  ║  🌇 Sunset    : {sunset}                     ║
  ╚══════════════════════════════════════╝
    """)
    
def get_forecast(city):
    url    = f"{BASE_URL}/forecast"
    params = {"q": city, "appid": API_KEY, "units": UNITS, "cnt": 40}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  Forecast error: {e}")
        return None


def display_forecast(data):
    print("\n  📅 5-Day Forecast")
    print("  " + "-" * 50)
    print(f"  {'DATE':<12} {'CONDITION':<20} {'MIN':>6} {'MAX':>6}")
    print("  " + "-" * 50)

    daily = {}
    for item in data["list"]:
        date = item["dt_txt"][:10]
        temp = item["main"]["temp"]
        desc = item["weather"][0]["description"].title()

        if date not in daily:
            daily[date] = {"min": temp, "max": temp, "desc": desc}
        else:
            daily[date]["min"] = min(daily[date]["min"], temp)
            daily[date]["max"] = max(daily[date]["max"], temp)

    for date, info in list(daily.items())[:5]:
        print(f"  {date:<12} {info['desc']:<20} {info['min']:>5.1f}° {info['max']:>5.1f}°")
    print()
    
def load_favs():
    if not FAVS_FILE.exists():
        return []
    return json.loads(FAVS_FILE.read_text()) if FAVS_FILE.read_text().strip() else []

def save_favs(favs):
    FAVS_FILE.write_text(json.dumps(favs, indent=2))

def add_favourite(city):
    favs = load_favs()
    if city.lower() in [f.lower() for f in favs]:
        print(f"  '{city}' is already in favourites.")
        return
    favs.append(city)
    save_favs(favs)
    print(f"  ✓ Added '{city}' to favourites.")

def show_favourites():
    favs = load_favs()
    if not favs:
        print("  No favourite cities yet.")
        return
    print("\n  ⭐ Favourite Cities:")
    for i, city in enumerate(favs, 1):
        print(f"    {i}. {city}")
    print()
    
def menu():
    print("\n  🌤  WEATHER APP")
    print("  " + "=" * 25)
    print("  1. Current weather")
    print("  2. 5-day forecast")
    print("  3. Weather for favourites")
    print("  4. Add to favourites")
    print("  5. Show favourites")
    print("  6. Exit")


def main():
    if API_KEY == "your_api_key_here":
        print("\n  ⚠  Please add your API key in the script first.")
        print("  Get a free key at: https://openweathermap.org/api\n")
        return

    while True:
        menu()
        choice = input("\n  Choose (1-6): ").strip()

        if choice == "1":
            city = input("  Enter city name: ").strip()
            data = get_weather(city)
            if data:
                display_weather(data)

        elif choice == "2":
            city = input("  Enter city name: ").strip()
            data = get_forecast(city)
            if data:
                display_forecast(data)

        elif choice == "3":
            favs = load_favs()
            if not favs:
                print("  No favourites yet. Add one first.")
            else:
                for city in favs:
                    data = get_weather(city)
                    if data:
                        display_weather(data)

        elif choice == "4":
            city = input("  Enter city name: ").strip()
            add_favourite(city)

        elif choice == "5":
            show_favourites()

        elif choice == "6":
            print("\n  Goodbye! 👋\n")
            break

        else:
            print("  Invalid choice. Enter 1 to 6.")


if __name__ == "__main__":
    main()