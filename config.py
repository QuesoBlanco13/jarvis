from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/")
    CALENDAR_FILE: str = os.getenv("CALENDAR_FILE", "data/calendar.json")

settings = Settings()
