# FZJ-Weather Prometheus Exporter
The FZJ-Weather Prometheus Exporter (short: exporter) is an exporter compatible with the Prometheus database.
It consists of two parts:
  1. `fzj_weather.py`: a python script using BeautifulSoup4 and requests to 
     parse and return meteorological data from a weather station inside the 
     Forschungszentrum Jülich (short: FZJ). It does so by parsing the website providing the information.
  2. exporter (`main.py`): uses said script to receive, parse and provide 
     the data to the Prometheus database. Once started, it runs indefinitely until interrupt.

`main.py` references the weather script and other needed scripts. It 
therefore marks the entry point of the exporter.

# Installing
1. Install the package from the corresponding Github Repository:
    `pip install git+https://github.com/o-druska/fzj-weather-prometheus-exporter`
2. Start the exporter:
    `prometheus_fzj_weather_exporter`

# Testing:
To test the exporter, you can host the script on your own machine:
  1. `prometheus_fzj_weather_exporter`
  2. (from another terminal) `curl 127.0.0.1:9840`
  
Running `curl 127.0.0.1:9840` should give you an output of similar 
structure like this:
```
# HELP fzj_weather_air_temperature temperature in celsius
# TYPE fzj_weather_air_temperature gauge
fzj_weather_air_temperature 14.0
```
The default port in the script is 9840.
Change the port with `prometheus_fzj_weather_exporter --port <port>`

(The output should be similar for other data points, i.e. humidity)
