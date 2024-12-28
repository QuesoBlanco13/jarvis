import requests
from config import settings

class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    async def get_weather(self, city: str):
        if not self.api_key:
            raise ValueError("OpenWeather API key not configured")

        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            weather_data = response.json()
            
            # Format the response
            return {
                "city": city,
                "temperature": weather_data["main"]["temp"],
                "description": weather_data["weather"][0]["description"],
                "humidity": weather_data["main"]["humidity"],
                "wind_speed": weather_data["wind"]["speed"]
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Weather service error: {str(e)}")
