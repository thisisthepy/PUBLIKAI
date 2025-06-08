def get_weather(location: str, unit: str = "celsius") -> str:
    """
    Get current weather information for a specified location.

    Args:
        location (str): The location for which to retrieve weather information.
        unit (str, optional): The unit of measurement for temperature. Default is "celsius".

    Returns:
        str: A string containing the current weather information for the specified location.

    Raises:
        ValueError: If the unit is not "celsius" or "fahrenheit".
    """
    # This is a placeholder implementation. In a real application, you would call a weather API.
    if unit not in ["celsius", "fahrenheit"]:
        raise ValueError("Unit must be 'celsius' or 'fahrenheit'.")

    # Simulated weather data
    weather_data = {
        "location": location,
        "temperature": 20 if unit == "celsius" else 68,  # Example temperature
        "unit": unit,
        "condition": "Sunny"
    }

    return f"The current weather in {location} is {weather_data['temperature']}°{unit[0].upper()} with {weather_data['condition']} conditions."
