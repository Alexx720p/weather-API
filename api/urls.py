from django.urls import path, include
from .views import WeatherView
from rest_framework import routers
from . import views

# router=routers.DefaultRouter()
# router.register(r'weather', views.WeatherView)


urlpatterns= [
    path('weather/<str:city>/', WeatherView.as_view(), name='weather'),
]