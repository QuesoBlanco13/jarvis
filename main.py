from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from modules.code_assistant import CodeAssistant
from modules.schedule_manager import ScheduleManager
from modules.weather_service import WeatherService
from config import settings

app = FastAPI(title="Personal AI Assistant")
