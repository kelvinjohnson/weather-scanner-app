from django.shortcuts import render, redirect
import requests
import config
from .models import City
from .forms import CityForm


def index(request):

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    error_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name'].capitalize()
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                response = requests.get(url.format(new_city, config.api_key)).json()

                if response['cod'] == 200:
                    form.save()
                else:
                    error_msg = 'Sorry, that city does not exist!'
            else:
                error_msg = 'That city has already been added!'
        if error_msg:
            message = error_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

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

    context = {
        'weather_info': weather_info,
        'form': form,
        'message': message,
        'message_class': message_class,
    }

    return render(request, 'index.html', context,)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')

