import requests
from django.conf import settings
from django.core.cache import cache

WEATHERLINK_API_KEY = getattr(settings, 'WEATHERLINK_API_KEY', None)
WEATHERLINK_API_SECRET = getattr(settings, 'WEATHERLINK_API_SECRET', None)


class WeatherLinkApi:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.base_url = 'https://api.weatherlink.com/v2/'

        self.headers = {
            "X-Api-Secret": api_secret
        }

    def get_stations(self):
        if cache.get('weatherlink_stations'):
            return cache.get('weatherlink_stations')
        else:
            url = f'{self.base_url}stations?api-key={self.api_key}'
            response = requests.get(url, headers=self.headers)

            response.raise_for_status()

            data = response.json().get('stations', [])
            # cache for 5 minutes
            cache.set('weatherlink_stations', data, 300)
            return response.json()

    def get_station(self, station_id):
        url = f'{self.base_url}station/{station_id}?api-key={self.api_key}'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_sensor_catalog(self):
        if cache.get('weatherlink_sensor_catalog'):
            return cache.get('weatherlink_sensor_catalog')

        url = f'{self.base_url}sensor-catalog?api-key={self.api_key}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        data = response.json().get('sensor_types', [])

        # cache for 24 hours
        cache.set('weatherlink_sensor_catalog', data, 86400)

        return data

    def get_current(self, station_id):
        url = f'{self.base_url}current/{station_id}?api-key={self.api_key}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


weatherlink_api = WeatherLinkApi(WEATHERLINK_API_KEY, WEATHERLINK_API_SECRET)
