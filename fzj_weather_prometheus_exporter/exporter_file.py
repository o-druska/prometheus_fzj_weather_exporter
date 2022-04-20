#!/usr/bin/env python3

from prometheus_client import Summary
from prometheus_client.core import GaugeMetricFamily

from fzj_weather_crawler import fzj_weather_crawler

REQUEST_TIME = Summary()


class FZJWeatherExporter:

    @REQUEST_TIME.time()
    def collect(self):
        weather = fzj_weather_crawler()

        g = GaugeMetricFamily(
            'fzjweather_temperature_celcius', 'temperature in celcius')
        g.add_metric([], weather.temperature)
        yield g

        g = GaugeMetricFamily(
            'fzjweather_air_pressure_hectopascal',
            'air pressure in hectopascal')
        g.add_metric([], weather.air_pressure)
        yield g

        g = GaugeMetricFamily(
            'fzjweather_humidity_percent', 'humidity in percent')
        g.add_metric([], weather.humidity)
        yield g

        g = GaugeMetricFamily(
            'fzjweather_wind_power_beaufort', 'wind power in beaufort')
        g.add_metric([], weather.wind_power)
        yield g

        g = GaugeMetricFamily(
            'fzjweather_wind_direction_degree', 'wind direction in degree')
        g.add_metric([], weather.wind_direction)
        yield g

        g = GaugeMetricFamily(
            'fzjweather_velocity_meter_per_second',
            'wind velocity in metres per second')
        g.add_metric([], weather.velocity_ms)
        yield g

        g = GaugeMetricFamily(
            'fzjweather_velocity_kilometer_per_hour',
            'wind velocity in kilometres per hour')
        g.add_metric([], weather.velocity_kmh)
        yield g
