import requests
from django.conf import settings
from django.core.cache import cache

WEATHERLINK_API_KEY = getattr(settings, 'WEATHERLINK_API_KEY', None)
WEATHERLINK_API_SECRET = getattr(settings, 'WEATHERLINK_API_SECRET', None)


# API Reference: https://weatherlink.github.io/v2-api/api-reference
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

            stations_data = response.json().get('stations', [])

            stations_data_dict_by_id = {}
            for station in stations_data:
                stations_data_dict_by_id[station['station_id']] = station

            # cache for 24 hours
            cache.set('weatherlink_stations', stations_data_dict_by_id, 86400)

            return stations_data_dict_by_id

    def get_station(self, station_id):

        stations = self.get_stations()

        if not stations.get(station_id):
            return None

        return stations.get(station_id)

    def get_sensors(self):
        if cache.get('weatherlink_sensors'):
            return cache.get('weatherlink_sensors')

        url = f'{self.base_url}sensors?api-key={self.api_key}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        sensors = response.json().get('sensors', [])
        sensors_dict_by_station = {}

        for sensor in sensors:
            station_id = sensor['station_id']
            if sensors_dict_by_station.get(station_id):
                sensors_dict_by_station[station_id].append(sensor)
            else:
                sensors_dict_by_station[station_id] = [sensor]

        # cache for 24 hours
        cache.set('weatherlink_sensors', sensors_dict_by_station, 86400)

        return sensors_dict_by_station

    def get_sensors_for_station(self, station_id):
        sensors = self.get_sensors()
        return sensors.get(station_id, [])

    def get_sensor_catalog(self):
        if cache.get('weatherlink_sensor_catalog'):
            return cache.get('weatherlink_sensor_catalog')

        url = f'{self.base_url}sensor-catalog?api-key={self.api_key}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        sensor_types_data = response.json().get('sensor_types', [])

        data_dict_by_sensor_type = {}
        for sensor_type in sensor_types_data:
            data_dict_by_sensor_type[sensor_type['sensor_type']] = sensor_type

        # cache for 24 hours
        cache.set('weatherlink_sensor_catalog', data_dict_by_sensor_type, 86400)

        return data_dict_by_sensor_type

    def get_sensor_catalog_for_sensor_type(self, sensor_type):
        sensor_catalog = self.get_sensor_catalog()
        return sensor_catalog.get(sensor_type, {})

    def get_sensor_catalog_for_station(self, station_id):
        sensors = self.get_sensors_for_station(station_id)

        catalog = []

        for sensor in sensors:
            sensor_catalog = self.get_sensor_catalog_for_sensor_type(sensor['sensor_type'])
            # dont include health sensors
            if sensor_catalog.get('category') == "Health":
                continue
            catalog.append(sensor_catalog)

        return catalog

    def get_current_conditions(self, station_id):
        url = f'{self.base_url}current/{station_id}?api-key={self.api_key}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


weatherlink_api = WeatherLinkApi(WEATHERLINK_API_KEY, WEATHERLINK_API_SECRET)
