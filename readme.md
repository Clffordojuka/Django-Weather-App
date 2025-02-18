# Weather App (Django)

## Overview
This Django-based Weather App fetches real-time weather data using the OpenWeatherMap API. Users can enter a city name and get weather details such as temperature, humidity, wind speed, and cloudiness.

## Features
- Fetch real-time weather data
- User-friendly interface with city input
- Secure API key management with `.env`
- Styled using `static/style.css`

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/your-username/weather-app.git
cd weather-app
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure the `.env` File
Create a `.env` file in the project root (same level as `manage.py`) and add your OpenWeather API key:
```env
WEATHER_API_KEY=your_actual_api_key_here
```
Replace `your_actual_api_key_here` with your OpenWeather API key.

### 5. Run Database Migrations
```sh
python manage.py migrate
```

### 6. Start the Development Server
```sh
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

## Project Structure
```
weather_project/
│── weather_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│── weather/
│   ├── templates/
│   │   ├── index.html
│   ├── static/
│   │   ├── style.css
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│── .env
│── manage.py
│── requirements.txt
│── README.md
```

## API Integration
This project uses the OpenWeatherMap API. The request is made as follows:
```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)
    return response.json()
```

## Troubleshooting
### 1. API Key Issues
If you see `401 Unauthorized`, ensure:
- The `.env` file is correctly formatted
- The API key is valid and active
- Restart the server after making changes

### 2. Static Files Not Loading
Run:
```sh
python manage.py collectstatic
```

## Contribution
Feel free to submit issues or pull requests on GitHub!

## License
This project is open-source under the MIT License.

