import os

import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_WEATHER')


def fetch_weather(city):
    """Получаем температуру в градусах Цельсия в указанном городе"""
    url = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=yes'
    response = requests.get(url)
    data = response.json()
    return data['current']['temp_c']
