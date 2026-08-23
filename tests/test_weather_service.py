import pytest
from unittest.mock import patch, MagicMock
from app.weather_service import get_current_weather


@patch("app.weather_service.requests.get")
def test_get_current_weather_success(mock_get):
    """Test successful weather data retrieval"""
    # Mock the API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "name": "Dublin",
        "sys": {"country": "IE"},
        "main": {
            "temp": 15.5,
            "feels_like": 14.2,
            "humidity": 72
        },
        "weather": [{"description": "partly cloudy"}],
        "wind": {"speed": 3.5}
    }
    mock_get.return_value = mock_response

    # Call the function
    result = get_current_weather("Dublin")

    # Assertions
    assert result["city"] == "Dublin"
    assert result["country"] == "IE"
    assert result["temperature"] == 15.5
    assert result["feels_like"] == 14.2
    assert result["humidity"] == 72
    assert result["description"] == "partly cloudy"
    assert result["wind_speed"] == 3.5
    
    # Verify the API was called correctly
    mock_get.assert_called_once()
    call_args = mock_get.call_args
    assert call_args[0][0] == "https://api.openweathermap.org/data/2.5/weather"


@patch("app.weather_service.requests.get")
def test_get_current_weather_api_error(mock_get):
    """Test handling of API errors"""
    # Mock an HTTP error response
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("API Error")
    mock_get.return_value = mock_response

    # Should raise an exception
    with pytest.raises(Exception):
        get_current_weather("NonexistentCity")


@patch("app.weather_service.requests.get")
def test_get_current_weather_response_structure(mock_get):
    """Test that the response has the expected structure"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "name": "London",
        "sys": {"country": "GB"},
        "main": {
            "temp": 12.0,
            "feels_like": 11.0,
            "humidity": 65
        },
        "weather": [{"description": "rainy"}],
        "wind": {"speed": 5.2}
    }
    mock_get.return_value = mock_response

    result = get_current_weather("London")

    # Check all expected keys are present
    expected_keys = {
        "city", "country", "temperature", "feels_like",
        "humidity", "description", "wind_speed"
    }
    assert set(result.keys()) == expected_keys
