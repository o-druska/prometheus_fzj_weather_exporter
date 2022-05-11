# FZJ-Weather Prometheus Exporter
The FZJ-Weather Prometheus Exporter (short: exporter) is an exporter compatible with the Prometheus database.
It consists of two parts:
  1. `fzj_weather.py`: a python script using BeautifulSoup4 and requests to parse and return meteorological data from a weather station inside of the Forschungszentrum Jülich (short: FZJ). It does so by parsing the website providing the information.
  2. exporter (`main.py`): uses said script to receive, parse and provide the data to the Prometheus database. Once started, it runs indefinetly until interrupt.

`main.py` references the weather script and other needed scripts. It therfore marks the entry point of the exporter.

# Exporter is currently under development
The exporter is not finished yet and full functionality is not guaranteed yet.

# Installing
1. Clone the Github repository:
    `git clone https://github.com/o-druska/fzj-weather-prometheus-exporter.git`
2. Install all the needed packages:
    `pip install fzj-weather-prometheus-exporter/.` (must be executed in top level dir of the project)
3. Start the exporter:
    `fzj_weather_exporter`

# Testing:
To test the exporter, you can host the script on your own machine:
  1. `python3 main.py`
  2. (from another terminal) `curl 127.0.0.1:9840`
Alternatively: install the exporter via pip (see above); then start using `fzj_weather_exporter`

The default port in the script is 9840.
Change the port with `python3 main.py --port xxxx`
Running the second command should give you an output of similar structure like this:
```
# HELP fzj_weather_air_temperature temperature in celsius
# TYPE fzj_weather_air_temperature gauge
fzj_weather_air_temperature 14.0
```

(The output shoudl be similar for other data points, i.e. humidity)
