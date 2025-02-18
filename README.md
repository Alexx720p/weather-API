# weather-API

https://roadmap.sh/projects/weather-api-wrapper-service

I used: 
  -Django
  -Django RestFramework
  -Redis
  -Docker


-Clone this repo 
-Move to the app: cd weatherapi
-Install dependencies: pip install -r requirements.txt
-Set your api key (I used Visual Crossing https://www.visualcrossing.com/weather-api/ )
-Run the project: python manage.py runserver  
  (go to your browser and write localhost:8000/weather/London/) #replace London with any city you want
-Or using Docker: docker-compose up --build (it will be executed in the localhost:8000, write the same link given above: localhost:8000/weather/London/ )
