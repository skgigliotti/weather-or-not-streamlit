import openmeteo_requests

import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
OPEN_MATEO_URL = "https://api.open-meteo.com/v1/forecast"

class Location:
    def __init__(self, lat, lng, **kwargs):
        self.lat = lat
        self.lng = lng
        self.elevation_asl = None
        self.temperature = None
        self.apparent_temperature = None
        self.relative_humidity = None
        self.precipitation_probability = None
        self.cloud_cover = None
        self.uv_index = None
        self.wind_speed = None
        self.wind_gusts = None
    
    def get_hourly_stats(self):
        data_fields = [
            "apparent_temperature",
            "cloud_cover",
            "precipitation_probability",
            "relative_humidity_2m",
            "temperature_2m",
            "uv_index",
            "wind_speed_10m",
            "wind_gusts_10m"]
        params = {
            "latitude": self.lat,
            "longitude": self.lng,
            "hourly": data_fields,
            "timezone": "America/Los_Angeles",
            "forecast_hours": 1,
            "wind_speed_unit": "mph",
	        "temperature_unit": "fahrenheit",
	        "precipitation_unit": "inch"
        }
        responses = openmeteo.weather_api(OPEN_MATEO_URL, params=params)
        response = responses[0]
        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()

        self.apparent_temperature = hourly.Variables(0).ValuesAsNumpy()[0]
        self.cloud_cover = hourly.Variables(1).ValuesAsNumpy()[0]
        self.precipitation_probability = hourly.Variables(2).ValuesAsNumpy()[0]
        self.relative_humidity = hourly.Variables(3).ValuesAsNumpy()[0]
        self.temperature = hourly.Variables(4).ValuesAsNumpy()[0]
        self.uv_index = hourly.Variables(5).ValuesAsNumpy()[0]
        self.wind_speed = hourly.Variables(6).ValuesAsNumpy()[0]
        self.wind_gusts = hourly.Variables(7).ValuesAsNumpy()[0]
