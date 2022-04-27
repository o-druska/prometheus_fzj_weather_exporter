#!/usr/bin/env python3

from prometheus_client import Summary
from prometheus_client.core import GaugeMetricFamily

from fzj_weather_prometheus_exporter import fzj_weather_crawler

REQUEST_TIME = Summary("weather_exporter_collect_seconds",
                       "Time spent to collect metrics from fzj_weather.py")


class FZJWeatherExporter:

    @REQUEST_TIME.time()
    def collect(self):
        weather = fzj_weather_crawler.fzj_weather_crawler()

        g = GaugeMetricFamily(
            name='fzj_weather_air_temperature_celsius',
            documentation='temperature in celcius')
        g.add_metric([], weather.temperature)
        yield g

        g = GaugeMetricFamily(
            name='fzj_weather_air_pressure_hectopascal',
            documentation='air pressure in hectopascal')
        g.add_metric([], weather.air_pressure)
        yield g

        g = GaugeMetricFamily(
            name='fzj_weather_humidity_percent',
            documentation='humidity in percent')
        g.add_metric([], weather.humidity)
        yield g

        g = GaugeMetricFamily(
            name='fzj_weather_wind_power_beaufort',
            documentation='wind power in beaufort')
        g.add_metric([], weather.wind_power)
        yield g

        g = GaugeMetricFamily(
            name='fzj_weather_wind_direction_degree',
            documentation='wind direction in degree')
        g.add_metric([], weather.wind_direction)
        yield g

        g = GaugeMetricFamily(
            name='fzj_weather_velocity_meters_per_second',
            documentation='wind velocity in meters per second')
        g.add_metric([], weather.velocity_ms)
        yield g

        g = GaugeMetricFamily(
            name='fzj_weather_velocity_kilometers_per_hour',
            documentation='wind velocity in kilometers per hour')
        g.add_metric([], weather.velocity_kmh)
        yield g
