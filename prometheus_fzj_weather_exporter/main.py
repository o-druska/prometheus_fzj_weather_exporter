#!/usr/bin/env python3
# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE.txt

# exporter entry point

# usage:    > python3 main.py --port :9840
# test:     > curl 127.0.0.1:9840
# (test in a different console or start in background)
# expected output (similar to):
# > # HELP fzj_weather_air_temperature temperature in celsius
# > # TYPE fzj_weather_air_temperature gauge
# > fzj_weather_air_temperature 14.0
# (equivalent output for other data i.e. humidity)

import argparse
import time
from prometheus_client import start_http_server, REGISTRY
from . import exporter_file


def main():
    args = get_parsed_args()

    REGISTRY.register(exporter_file.FZJWeatherExporter())
    start_http_server(args.port)

    # keep the thing going indefinitely
    while True:
        time.sleep(1)


def get_parsed_args():
    parser = argparse.ArgumentParser(
        description='Set up the Prometheus exporter (connection ports)')
    parser.add_argument(
        '-p', '--port',
        type=int,
        dest='port',
        default=9840,
        help='Port to run the script on')

    return parser.parse_args()


if __name__ == '__main__':
    main()
