import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.weather_service import get_current_weather

app = FastAPI(
    title="Weatherwise API",
    description="A simple weather API built with FastAPI",
    version="1.0.0"
)


@app.get("/")
def read_root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Weatherwise API",
        "endpoints": {
            "weather": "/weather/{city}",
            "health": "/health"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/weather/{city}")
def get_weather(city: str):
    """
    Get current weather for a city.
    
    Args:
        city: City name (e.g., "Dublin", "London")
        
    Returns:
        Weather data including temperature, humidity, description, etc.
    """
    try:
        weather_data = get_current_weather(city)
        return weather_data
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"City '{city}' not found"
            )
        raise HTTPException(
            status_code=e.response.status_code,
            detail="Failed to fetch weather data"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )