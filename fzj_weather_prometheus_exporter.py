#!/usr/bin/env python3
# exporter entry point

import argparse
import time

from prometheus_client import start_http_server, REGISTRY
import fzj_weather_prometheus_exporter
from .fzj_weather_prometheus_exporter import exporter_file


"""
note: run this using: (-p for the Prometheus port)
> python3 my_exporter.py -p :9840


You can test wether it works from another console window using:
> curl 127.0.0.1:9840


This should give the following output:
> # NAME fzjweather_temperature_celcius
> # HELP temperature in celcius
> fzjweather_temperature_celcius{instance='bla.bla.bla'} 12.0
> # NAME fzjweather_humidity_percent
> # HELP humidity value blabla
> fzjweather_humidity_percent{instance='bla.bla.bla'} 52
"""


def main():
    parser = argparse.ArgumentParser(
        description='Set up the Prometheus exporter (connection ports, etc.)')
    parser.add_argument(
        '-p', '--port',
        dest='port',
        type='str',
        default=':9840',
        help='Port to listen on')
    args = parser.parse_args()

    REGISTRY.register(fzj_weather_prometheus_exporter.
                      exporter_file.FZJWeatherExporter())
    start_http_server(args.port)

    # keep the thing going indefinitely
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
