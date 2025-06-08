import requests
import json
from typing import Dict, Any
from datetime import datetime


class WeatherAPI:
    """Weather API wrapper using Open-Meteo (free service, no API key required)."""
    
    def __init__(self):
        """Initialize Weather API client."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://api.open-meteo.com/v1"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    
    def get_coordinates(self, location: str) -> Dict[str, Any]:
        """
        Get coordinates for a location using Open-Meteo geocoding API.
        
        Args:
            location: City name or location
            
        Returns:
            Dict with latitude, longitude, and location info
        """
        try:
            params = {
                'name': location,
                'count': 1,
                'language': 'en',
                'format': 'json'
            }
            
            response = self.session.get(self.geocoding_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('results'):
                return {"error": f"Location '{location}' not found"}
            
            location_data = data['results'][0]
            return {
                "latitude": location_data['latitude'],
                "longitude": location_data['longitude'],
                "name": location_data['name'],
                "country": location_data.get('country', ''),
                "admin1": location_data.get('admin1', ''),  # State/Province
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Geocoding request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Geocoding error: {str(e)}"}
    
    def get_weather_data(self, location: str, unit: str = "celsius") -> Dict[str, Any]:
        """
        Get current weather data using Open-Meteo API.
        
        Args:
            location: City name
            unit: Temperature unit (celsius/fahrenheit)
            
        Returns:
            Dict containing weather data or error
        """
        try:
            # Get coordinates first
            coord_data = self.get_coordinates(location)
            if "error" in coord_data:
                return coord_data
            
            # Get current weather
            params = {
                'latitude': coord_data['latitude'],
                'longitude': coord_data['longitude'],
                'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m,surface_pressure',
                'timezone': 'auto'
            }
            
            if unit == "fahrenheit":
                params['temperature_unit'] = 'fahrenheit'
            
            response = self.session.get(f"{self.base_url}/forecast", params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            current = data.get('current', {})
            
            # Map weather code to condition
            weather_code = current.get('weather_code', 0)
            condition = self._get_weather_condition(weather_code)
            
            return {
                "location": coord_data['name'],
                "country": coord_data['country'],
                "admin1": coord_data['admin1'],
                "temperature": round(current.get('temperature_2m', 0), 1),
                "unit": unit,
                "condition": condition,
                "humidity": int(current.get('relative_humidity_2m', 0)),
                "wind_speed": round(current.get('wind_speed_10m', 0), 1),
                "wind_direction": int(current.get('wind_direction_10m', 0)),
                "pressure": int(current.get('surface_pressure', 0)),
                "feels_like": round(current.get('apparent_temperature', 0), 1),
                "timestamp": current.get('time', datetime.now().isoformat()),
                "source": "Open-Meteo"
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Invalid response from weather service"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def get_forecast_data(self, location: str, days: int = 7, unit: str = "celsius") -> Dict[str, Any]:
        """
        Get weather forecast data using Open-Meteo API.
        
        Args:
            location: City name
            days: Number of days (1-16)
            unit: Temperature unit
            
        Returns:
            Dict containing forecast data or error
        """
        try:
            # Get coordinates first
            coord_data = self.get_coordinates(location)
            if "error" in coord_data:
                return coord_data
            
            # Get forecast
            params = {
                'latitude': coord_data['latitude'],
                'longitude': coord_data['longitude'],
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,wind_direction_10m_dominant',
                'timezone': 'auto',
                'forecast_days': min(days, 16)  # Open-Meteo supports up to 16 days
            }
            
            if unit == "fahrenheit":
                params['temperature_unit'] = 'fahrenheit'
            
            response = self.session.get(f"{self.base_url}/forecast", params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            daily = data.get('daily', {})
            
            if not daily:
                return {"error": "No forecast data available"}
            
            forecast_days = []
            for i in range(len(daily.get('time', []))):
                day_data = {
                    "date": daily['time'][i],
                    "weather_code": daily.get('weather_code', [])[i] if i < len(daily.get('weather_code', [])) else 0,
                    "max_temp": daily.get('temperature_2m_max', [])[i] if i < len(daily.get('temperature_2m_max', [])) else 0,
                    "min_temp": daily.get('temperature_2m_min', [])[i] if i < len(daily.get('temperature_2m_min', [])) else 0,
                    "precipitation": daily.get('precipitation_sum', [])[i] if i < len(daily.get('precipitation_sum', [])) else 0,
                    "wind_speed": daily.get('wind_speed_10m_max', [])[i] if i < len(daily.get('wind_speed_10m_max', [])) else 0,
                    "wind_direction": daily.get('wind_direction_10m_dominant', [])[i] if i < len(daily.get('wind_direction_10m_dominant', [])) else 0,
                }
                forecast_days.append(day_data)
            
            return {
                "location": coord_data['name'],
                "country": coord_data['country'],
                "admin1": coord_data['admin1'],
                "forecast_days": forecast_days,
                "unit": unit,
                "source": "Open-Meteo"
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Invalid response from weather service"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def _get_weather_condition(self, weather_code: int) -> str:
        """Convert Open-Meteo weather code to condition string."""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            56: "Light freezing drizzle", 57: "Dense freezing drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            66: "Light freezing rain", 67: "Heavy freezing rain",
            71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            85: "Slight snow showers", 86: "Heavy snow showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(weather_code, "Unknown")
    
    def _get_wind_direction_text(self, degrees: int) -> str:
        """Convert wind direction degrees to compass direction."""
        directions = [
            'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
            'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'
        ]
        index = int((degrees + 11.25) / 22.5) % 16
        return directions[index]


# Global weather API instance
weather_api = WeatherAPI()


def get_weather(location: str, unit: str = "celsius") -> str:
    """
    Get current weather information for a specified location.
    Uses Open-Meteo free service - no API key required.

    Args:
        location (str): The location for which to retrieve weather information.
        unit (str, optional): The unit of measurement for temperature. Default is "celsius".

    Returns:
        str: A string containing the current weather information for the specified location.

    Raises:
        ValueError: If the unit is not "celsius" or "fahrenheit".
    """
    if unit not in ["celsius", "fahrenheit"]:
        raise ValueError("Unit must be 'celsius' or 'fahrenheit'.")
    
    weather_data = weather_api.get_weather_data(location, unit)
    
    if "error" in weather_data:
        return f"Error getting weather for {location}: {weather_data['error']}"
    
    # Format the response
    unit_symbol = "°C" if unit == "celsius" else "°F"
    
    # Build location string
    location_str = weather_data['location']
    if weather_data.get('admin1'):
        location_str += f", {weather_data['admin1']}"
    if weather_data.get('country'):
        location_str += f", {weather_data['country']}"
    
    response = f"Current weather in {location_str}:\n"
    response += f"🌡️ Temperature: {weather_data['temperature']}{unit_symbol}"
    
    if weather_data.get('feels_like') and weather_data['feels_like'] != weather_data['temperature']:
        response += f" (feels like {weather_data['feels_like']}{unit_symbol})"
    
    response += f"\n☁️ Condition: {weather_data['condition']}\n"
    response += f"💧 Humidity: {weather_data['humidity']}%\n"
    
    # Wind with direction
    wind_dir = weather_api._get_wind_direction_text(weather_data['wind_direction'])
    response += f"💨 Wind: {weather_data['wind_speed']} m/s {wind_dir}\n"
    response += f"📊 Pressure: {weather_data['pressure']} hPa\n"
    response += f"📡 Source: {weather_data['source']}"
    
    return response


def get_weather_forecast(location: str, days: int = 7, unit: str = "celsius") -> str:
    """
    Get weather forecast for specified location.
    Open-Meteo provides up to 16 days of forecast data.
    
    Args:
        location: Location name
        days: Number of days to forecast (1-16, supported by Open-Meteo API)
        unit: Temperature unit
        
    Returns:
        Formatted forecast string
    """
    if unit not in ["celsius", "fahrenheit"]:
        raise ValueError("Unit must be 'celsius' or 'fahrenheit'.")
    
    if days < 1 or days > 16:
        days = min(max(days, 1), 16)  # Clamp between 1 and 16
    
    forecast_data = weather_api.get_forecast_data(location, days, unit)
    
    if "error" in forecast_data:
        return f"Error getting forecast for {location}: {forecast_data['error']}"
    
    unit_symbol = "°C" if unit == "celsius" else "°F"
    
    # Build location string
    location_str = forecast_data['location']
    if forecast_data.get('admin1'):
        location_str += f", {forecast_data['admin1']}"
    if forecast_data.get('country'):
        location_str += f", {forecast_data['country']}"
    
    response = f"Weather forecast for {location_str} ({days} days):\n\n"
    
    for day_data in forecast_data['forecast_days']:
        date = day_data['date']
        condition = weather_api._get_weather_condition(day_data['weather_code'])
        max_temp = round(day_data['max_temp'], 1)
        min_temp = round(day_data['min_temp'], 1)
        precipitation = round(day_data['precipitation'], 1)
        wind_speed = round(day_data['wind_speed'], 1)
        wind_dir = weather_api._get_wind_direction_text(int(day_data['wind_direction']))
        
        # Format date nicely
        try:
            date_obj = datetime.fromisoformat(date.replace('Z', '+00:00'))
            formatted_date = date_obj.strftime('%Y-%m-%d (%A)')
        except:
            formatted_date = date
        
        response += f"📅 {formatted_date}\n"
        response += f"   🌡️ High: {max_temp}{unit_symbol}, Low: {min_temp}{unit_symbol}\n"
        response += f"   ☁️ Condition: {condition}\n"
        
        if precipitation > 0:
            response += f"   🌧️ Precipitation: {precipitation} mm\n"
        
        response += f"   💨 Wind: {wind_speed} m/s {wind_dir}\n\n"
    
    response += f"📡 Source: {forecast_data['source']}"
    return response


# Example usage and test cases
if __name__ == '__main__':
    test_locations = ["Seoul", "New York", "London", "Tokyo", "Sydney"]
    test_forecast_days = [1, 3, 7, 10, 16]  # Test different forecast periods
    
    print("Weather API Test Results (Open-Meteo):")
    print("=" * 60)
    
    # Test current weather for multiple locations
    for location in test_locations:
        print(f"\nTesting current weather: {location}")
        print("-" * 40)
        
        result = get_weather(location)
        print(result)
        print()
    
    print("=" * 60)
    print("Forecast Tests - Different Day Ranges:")
    print("=" * 60)
    
    # Test different forecast periods
    test_location = "Seoul"
    for days in test_forecast_days:
        print(f"\nTesting {days}-day forecast for {test_location}:")
        print("-" * 50)
        
        forecast = get_weather_forecast(test_location, days)
        print(forecast)
        print()
    
    print("=" * 60)
    print("Unit Conversion Test:")
    print("=" * 60)
    
    # Test unit conversions
    test_location = "New York"
    print(f"\nCelsius forecast for {test_location} (7 days):")
    print("-" * 40)
    celsius_forecast = get_weather_forecast(test_location, 7, "celsius")
    print(celsius_forecast)
    
    print(f"\nFahrenheit forecast for {test_location} (7 days):")
    print("-" * 40)
    fahrenheit_forecast = get_weather_forecast(test_location, 7, "fahrenheit")
    print(fahrenheit_forecast)
    
    print("\n" + "=" * 60)
    print("Edge Case Tests:")
    print("=" * 60)
    
    # Test edge cases
    print("\nTesting invalid location:")
    print("-" * 30)
    invalid_result = get_weather("NonExistentCity12345")
    print(invalid_result)
    
    print("\nTesting extreme forecast days (25 days - should clamp to 16):")
    print("-" * 30)
    extreme_forecast = get_weather_forecast("Seoul", 25)
    # Count actual days in response
    day_count = extreme_forecast.count("📅")
    print(f"Requested 25 days, got {day_count} days (should be 16)")
    print(extreme_forecast[:500] + "..." if len(extreme_forecast) > 500 else extreme_forecast)
    
    print("\nTesting negative days (should clamp to 1):")
    print("-" * 30)
    negative_forecast = get_weather_forecast("Seoul", -5)
    day_count = negative_forecast.count("📅")
    print(f"Requested -5 days, got {day_count} days (should be 1)")
    print(negative_forecast)
