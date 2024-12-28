from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/")
    CALENDAR_FILE: str = os.getenv("CALENDAR_FILE", "data/calendar.json")

settings = Settings()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
code_assistant = CodeAssistant()
schedule_manager = ScheduleManager()
weather_service = WeatherService()

@app.get("/")
async def root():
    return {"message": "AI Assistant API is running"}

@app.post("/code/generate")
async def generate_code(prompt: str):
    try:
        return await code_assistant.generate_code(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather")
async def get_weather(city: str):
    try:
        return await weather_service.get_weather(city)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/schedule/add")
async def add_event(event: dict):
    try:
        return await schedule_manager.add_event(event)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
