from django.shortcuts import render
import requests
import config
from .models import City


def index(request):

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
    city = 'London'
    cities = City.objects.all()

    weather_info = []

    for city in cities:

        response = requests.get(url.format(city, config.api_key)).json()

        city_weather = {
            'city': city.name,
            'temperature': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }

        weather_info.append(city_weather)

    context = {'weather_info': weather_info}

    return render(request, 'index.html', context)

