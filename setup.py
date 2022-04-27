#!/usr/bin/env python3
''' setup file for installation of fzj_weather prometheus exporter '''
from setuptools import setup, find_packages

setup(
    name='fzj_weather_prometheus_exporter',
    version='0.0.1',
    description='prometheus exporter for weather data from FZJ',
    author='Oskar Druska',
    author_email='o.druska@fz-juelich.de',
    packages=find_packages(),
    license=,
    install_requires=[
        'requests',
        'BeautifulSoup4'
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'export_main=fzj-weather-prometheus-exporter/main.py:main'
        ],
    },

)
