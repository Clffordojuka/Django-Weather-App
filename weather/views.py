from django.shortcuts import render
from django.conf import settings
import requests
import logging
import datetime

def index(request):
    api_key = settings.WEATHER_API_KEY
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

    if request.method == 'POST':
        City1 = request.POST['City1']
        City2 = request.POST.get('City2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(City1, api_key, current_weather_url, forecast_url)

        if City2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(City2, api_key, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        # 🔹 Filter out cities with errors
        context = {
            'weather_data1': weather_data1 if weather_data1 else None,
            'daily_forecasts1': daily_forecasts1 if daily_forecasts1 else None,
            'weather_data2': weather_data2 if weather_data2 else None,
            'daily_forecasts2': daily_forecasts2 if daily_forecasts2 else None,
        }

        return render(request, 'weather/index.html', context)
    
    return render(request, 'weather/index.html')


logger = logging.getLogger(__name__)

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    # Fetch current weather
    response = requests.get(current_weather_url.format(city, api_key)).json()
    logger.info(f"Weather API Response for {city}: {response}")

    if response.get('cod') != 200:
        logger.warning(f"Skipping {city} - Current Weather API Error: {response.get('message')}")
        return None, None

    lat, lon = response['coord']['lat'], response['coord']['lon']

    # Fetch forecast data (switching to 'forecast' endpoint)
    forecast_response = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
    ).json()
    logger.info(f"Forecast API Response for {city}: {forecast_response}")

    if forecast_response.get('cod') != "200":
        logger.warning(f"Skipping {city} - Forecast API Error: {forecast_response.get('message')}")
        return None, None

    # Process current weather
    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    # Process forecast data
    daily_forecasts = []
    for item in forecast_response['list'][:5]:  # First 5 entries (approx. 1 day)
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(item['dt']).strftime('%A'),
            'min_temp': round(item['main']['temp_min'] - 273.15, 2),
            'max_temp': round(item['main']['temp_max'] - 273.15, 2),
            'description': item['weather'][0]['description'],
            'icon': item['weather'][0]['icon'],
        })

    return weather_data, daily_forecasts


