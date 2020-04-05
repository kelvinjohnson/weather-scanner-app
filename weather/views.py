from django.shortcuts import render


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metrics&appid='
    return render(request, 'index.html')

