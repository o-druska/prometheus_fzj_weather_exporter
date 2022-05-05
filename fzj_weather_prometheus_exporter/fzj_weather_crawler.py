#!/usr/bin/env python3
# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE.txt

from dataclasses import dataclass
from fzj_weather_prometheus_exporter import fzj_weather


@dataclass
class Weather:
    temperature: float  # celsius
    air_pressure: float  # hectoPascal
    humidity: int  # percent
    wind_power: int  # beaufort
    wind_direction: int  # degree


def fzj_weather_crawler():
    """ scrapes data from the FZJ weather site via the fzj_weather.py script
        and returns a dataclass object containing the information """
    crawled_weather_data = fzj_weather.get_weather_data()

    weather_return = Weather(
        temperature=crawled_weather_data['Lufttemperatur'],
        air_pressure=crawled_weather_data['Luftdruck (92 m ü.N.N.)'],
        humidity=crawled_weather_data['relative Feuchte'],
        wind_power=crawled_weather_data['Windstärke'],
        wind_direction=crawled_weather_data['Windrichtung']
    )
    return weather_return


if __name__ == '__main__':
    print(fzj_weather_crawler())
