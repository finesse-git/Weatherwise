from app.weather_service import get_current_weather

if __name__ == "__main__":
    weather = get_current_weather("Dublin")
    print(weather)