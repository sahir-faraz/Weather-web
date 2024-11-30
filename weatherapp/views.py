from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    city = request.POST.get('city', 'raichur')
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid='
    weather_params = {'units': 'metric'}
    
    api_key = 'AIzaSyAWWSyIi64k6-Cr9_SU5BIdJMZhTMpXzx0'
    search_engine_id = '77ef9b2c4a2654fc2'
    query = f"{city} 1920x1080"
    start = 1
    search_type = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}&start={start}&searchType={search_type}&imgSize=xlarge"

    image_url = None  # Default value in case no image is found
    try:
        data = requests.get(city_url).json()
        search_items = data.get("items")
        if search_items and len(search_items) >= 2:
            image_url = search_items[1].get('link')  # Retrieve the link of the second item
    except Exception as e:
        print(f"Error fetching image: {e}")

    try:
        data = requests.get(weather_url, params=weather_params).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        context = {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url,
        }
    except KeyError as e:
        print(f"KeyError: {e}")
        messages.error(request, 'Entered data is not available to API')
        city = 'raichur'
        try:
            data = requests.get(weather_url, params=weather_params).json()
            description = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            temp = data['main']['temp']
            day = datetime.date.today()
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            description = 'clear sky'
            icon = '01d'
            temp = 25
            day = datetime.date.today()

        context = {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': 'indore',
            'exception_occurred': True,
            'image_url': image_url,
        }

    return render(request, 'weatherapp/index.html', context)
#Devloped BY Sahir Faraz 2024