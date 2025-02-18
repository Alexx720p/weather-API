import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from .serializer import Weather_serializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
import logging
import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv('api_key')
logger=logging.getLogger(__name__)

class CustomAnonRateThrottle(AnonRateThrottle):
    rate='30/hour'

class WeatherView(APIView):
    throttle_classes=[CustomAnonRateThrottle]
    @method_decorator(cache_page(60*15))
    def get(self, request, city, format= None):
        cache_key=f'weather_{city}'
        cached_data=cache.get(cache_key)
        if cached_data:
            logger.info(f'Fetching weather data for city {city}')
            return Response(cached_data, status=status.HTTP_200_OK)

        url= f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={api_key}'
        
        try:
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            weather_data={
                'city': city,
                'temperature': data['currentConditions']['temp'],
                'description': data['currentConditions']['conditions']
            }
            serializer=Weather_serializer(weather_data)
            # cache.set(cache_key, serializer.data, timeout=60*15)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except requests.HTTPError as http_err:
            logger.error(f'HTTP error ocurred: {http_err}')
            return Response({'error': 'An error ocurred while fetching weather data. Please checkthe city name and try again'}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException as req_err:
            logger.error(f'Request error ocurred: {req_err}')
            return Response({'error': 'A network error ocurred. Please try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as json_err:
            logger.error(f'JSON decode error: {json_err}')
            return Response({'error': 'An error ocurred while processing the weather data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

