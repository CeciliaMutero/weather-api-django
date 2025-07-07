import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from decouple import config


# Create your views here.
@api_view(['GET'])
def get_weather(request):
    """
    Get current weather for a given city.
    Example: /api/weather/?city=Nairobi
    """
    print("DEBUG - request.GET:", request.GET)
    city = request.GET.get('city')  # Get ?city=Nairobi from URL
    if not city:
        return Response({"error": "City parameter is required"}, status=400)

    api_key = config('OPENWEATHER_API_KEY')
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return Response({"error": data.get("message", "Failed to fetch weather data")}, status=response.status_code)

        result = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
        }
        return Response(result)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
