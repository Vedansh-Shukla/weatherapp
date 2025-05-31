from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
import os

def webpage(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'new delhi'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=9d7734b4df2637bad46d1ca7271211f2'
    PARAMS = {'units': 'metric'}

    API_KEY = 'AIzaSyBUch4YCr2wuSrVceEN_wVD40hr8FqJEss'
    SEARCH_ENGINE_ID = '401b01f91c14b4412'

    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    data = requests.get(city_url).json()
    search_items = data.get("items", [])
    image_url = search_items[1]['link'] if len(search_items) > 1 else None

    try:
        data = requests.get(url, params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        return render(request, 'main4.html',
                      {'description': description, 'icon': icon, 'temp': temp, 'day': day, 'city': city,
                       'exception_occurred': False, 'image_url': image_url})

    except KeyError:
        exception_occurred = True
        messages.error(request, 'Entered data is not available to API')
        day = datetime.date.today()

        return render(request, 'main4.html',
                      {'description': 'clear sky', 'icon': '01d', 'temp': 25, 'day': day, 'city': 'indore',
                       'exception_occurred': exception_occurred})
