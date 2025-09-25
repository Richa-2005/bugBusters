import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime
from app import get_coordinates
def hello(assistant_output):
    return assistant_output
def generate_weather_advice(current_weather, daily_forecast):
    """
    Generates human-readable advice based on weather data.
    This acts as our 'AI' logic.
    """
    advice = []
    
    # Extract key metrics for decision making
    uvi = current_weather.get('uvi', 0)
    pop = daily_forecast.get('pop', 0) * 100  # Probability of precipitation
    day_temp = daily_forecast.get('temp', {}).get('day', 0)
    weather_condition = daily_forecast.get('weather', [{}])[0].get('main', '')

    # Advice based on UV Index
    if uvi > 7:
        advice.append(f"The UV index is high ({uvi}). Wear sunscreen and sunglasses if you'll be outside for a while.")
    elif uvi > 2:
        advice.append(f"The UV index is moderate ({uvi}). It's still a good idea to protect your skin.")

    # Advice based on precipitation
    if pop > 60:
        advice.append(f"There's a high chance of rain today ({pop:.0f}%). Don't forget your umbrella!")
    elif pop > 30:
        advice.append(f"There's a slight chance of rain ({pop:.0f}%). It might be a good idea to take an umbrella just in case.")

    # Advice based on temperature
    if day_temp > 32:
        advice.append(f"It's going to be very hot, around {day_temp}*C. Stay hydrated and avoid strenuous activity during peak hours.")
    
    # Advice based on general weather conditions
    if weather_condition == "Thunderstorm":
        advice.append("Thunderstorms are expected. It's best to stay indoors and avoid open areas.")
    elif weather_condition == "Clear":
        advice.append("Expect clear skies today, a perfect day for outdoor activities!")
    elif weather_condition in ["Rain", "Drizzle"]:
        advice.append("Rain is expected. Wear waterproof clothing if you plan to be outside.")

        
    # Default message if no other advice fits
    if not advice:
        advice.append("Weather conditions seem stable today. Enjoy your day!")

    return advice


def create_ai_assistant_json(lat, lon, api_key, filename="generalalert.json"):
    """
    Fetches weather data, generates advice, and saves it all to a JSON file.
    """
    # We need current and daily for our advice logic
    exclude_parts = "minutely,hourly,alerts"
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude_parts}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current_data = data.get('current', {})
        today_daily_data = data['daily'][0]

        # Generate our AI-powered advice
        advice_list = generate_weather_advice(current_data, today_daily_data)
        
        # Get the human-readable summary directly from the API
        friendly_summary = today_daily_data.get('summary', "A general weather overview for the day.")

        # Structure the final JSON output
        assistant_output = {
            "location": {
                "latitude": lat,
                "longitude": lon,
                "timezone": data.get('timezone', 'N/A')
            },
            "assistant_report": {
                "generated_at_utc": datetime.utcfromtimestamp(current_data.get('dt')).isoformat() + 'Z',
                "friendly_summary": friendly_summary,
                "advice": advice_list,
                "key_metrics": {
                    "current_temp_celsius": current_data.get('temp'),
                    "current_condition": current_data.get('weather', [{}])[0].get('description', 'N/A').title(),
                    "chance_of_rain_percent": today_daily_data.get('pop', 0) * 100,
                    "max_temp_celsius": today_daily_data.get('temp', {}).get('max'),
                    "min_temp_celsius": today_daily_data.get('temp', {}).get('min')
                }
            }
        }

        # Save the structured output to a JSON file
        # with open(filename, 'w') as json_file:
        #     json.dump(assistant_output, json_file, indent=4)
        hello()
        return f"AI Weather Assistant report successfully saved to {filename}"

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except (KeyError, IndexError):
        return "Error: Could not parse the weather data from the API response."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("OPEN_WEATHER_API_KEY")
    
    if not api_key:
        print("Error: OPEN_WEATHER_API_KEY not found in .env file.")
    else:
        
        lat, lon = get_coordinates()
        result_message = create_ai_assistant_json(lat, lon, api_key)
        print(result_message)
