import requests
from django.shortcuts import render
from .models import City


def index(request):
    appid = 'f381181aa51f1eab6aee277b87c2640d'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&lang=ru&units=metric&appid=' + appid

    if request.method == 'POST':
        city = City()
        city.name = request.POST.get('name')
        city.save()

    cities = City.objects.all()
    all_cities = []

    for city in cities:
        response = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': int(response["main"]["temp"]),
            'description': response['weather'][0]['description'],
            'icon': response["weather"][0]["icon"],
            'min': int(response["main"]["temp_min"]),
            'max': int(response["main"]["temp_max"]),
            'feels': int(response["main"]["feels_like"]),
            'humidity': int(response["main"]["humidity"]),
        }

        all_cities.append(city_info)
        all_cities.reverse()

    context = {'all_info': all_cities}

    return render(request, 'weather/index.html', context)

