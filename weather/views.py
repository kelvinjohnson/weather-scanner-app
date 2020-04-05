from django.shortcuts import render
import requests
import config
from .models import City
from .forms import CityForm


def index(request):

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

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

    context = {'weather_info': weather_info, 'form': form}

    return render(request, 'index.html', context,)

