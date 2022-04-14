#!/usr/bin/env python3

# This script extracts weather data from the FZJ-inside weather station.
# Output can be specified with arguments.

import argparse
import requests
from bs4 import BeautifulSoup


# Python module to execute

def main():
    url = "https://www.fz-juelich.de/gs/DE/UeberUns/Organisation/S-U/Meteorologie/wetter/wd402_node.html"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    args = parseargs()

    weather_dict = make_weather_dict(url, soup)  # {header: data}

    # configures arg-dependent states of other arguments
    # (such as --inverse in inverts every args boolean status)
    config_args(args)

    if args.order is None:
        ret = value_to_string(args, weather_dict, r)
        return ret
    else:
        ret = value_to_string_order(args, weather_dict, r, args.order)
        return ret


def make_weather_dict(url, soup):
    # Parses the table containing the needed information to get all table rows.
    weather_tablerows = soup.table.find_all("tr")

    # Creates a dictionary with headers as keys and data as values
    # (i.e. Luftdruck: 1016.6 hPa).
    # `.replace(u'\xa0', u' ')` replaces parsing errors with whitespaces
    weather_data = {
        "source": url,
        "title": soup.title.get_text(strip=True),
        "date": soup.u.get_text(strip=True)
    }

    for row in weather_tablerows:
        weather_td = row.find_all("td")  # td, table data

        weather_data[weather_td[0].get_text(strip=True).replace(u'\xa0', u' ')] \
            = weather_td[1].get_text(strip=True).replace(u'\xa0', u' ')

    return weather_data


def parseargs():
    parser = argparse.ArgumentParser(
        description='This program´s purpose is to retrieve meteorological data from FZJ internal weather station.\n'
                    'The usage of arguments specifies the given output (view below).\n'
                    '-H makes output less humanly readable; i.e. for easier usage in data administration.\n'
                    'If no arguments are specified, a default output is given.\n'
                    'Default output is all values.\n'
                    'Output order can be specified with the -o option,'
                    'by appending a string consisting of the data abbreviations;'
                    'i.e. `-o pt` for air pressure, then temperature.\n'
                    'Beaufort to m/s conversion: v = 0.836 * (Bf^(3/2))\n'
                    'All values but wind speed in km/h and m/s are parsed directly from the website.\n'
                    'Wind speed in km/h and m/s may contain conversion errors due to Bf to m/s conversion.')

    meta_group = parser.add_argument_group()
    data_group = parser.add_argument_group()

    # meta_group consists of arguments, which toggle meta information about output
    meta_group.add_argument(
        '-b', '--debug',
        action='store_true',
        help='provides debug information to help adjust the script, '
             'in case of changes in sourcecode, etc.',
        default=False)
    meta_group.add_argument(
        '-H', '--Human',
        action='store_true',
        help='output is less humanly readable; just prints numbers w/o any measures/units; '
             'better suited for script piping',
        default=False)
    meta_group.add_argument(
        '-i', '--inverse',
        help='inverts the boolean values of all data arguments before evaluation of said arguments is done; '
             'must be provided with a boolean value',
        default=False)
    meta_group.add_argument(
        '-o', '--order',
        help='modifies the order in which the data is printed;'
             'must be followed by the abbreviations for the data points;'
             'i.e.: `tpud` for temperature, air pressure, humidity and wind direction; in that order.',
        action='store',
        metavar='order_string',

    )

    # data_group consists of arguments to specify the output
    data_group.add_argument(
        '-t', '--temperature',
        action='store_true',
        help='prints temperature in celsius',
        default=False)
    data_group.add_argument(
        '-p', '--airpressure',
        action='store_true',
        help='prints air pressure in hectopascal',
        default=False)
    data_group.add_argument(
        '-u', '--humidity',
        action='store_true',
        help='prints relative humidity',
        default=False)
    data_group.add_argument(
        '-w', '--power',
        action='store_true',
        help='prints wind power in Beaufort',
        default=False)
    data_group.add_argument(
        '-d', '--direction',
        action='store_true',
        help='prints wind direction in degrees',
        default=False)
    data_group.add_argument(
        '-v', '--velocity',
        action='store_true',
        help='prints wind speed in metres per second',
        default=False)
    data_group.add_argument(
        '-s', '--speed',
        action='store_true',
        help='prints wind speed in kilometres per hour',
        default=False)

    return parser.parse_args()


def value_to_string(args, weather_dict, request):  # returns string
    weather_printout = ""

    # debug output; returns nothing but that
    if args.debug:
        print(request.status_code)  # prints server response
        weather_printout += (weather_dict['date']).replace("Aktuelle Messwerte vom ", "")  # temp solution
        weather_printout += "\n"
        weather_printout += (weather_dict['source']) + "\n"
        weather_printout += str((weather_dict.keys())) + "\n"
        weather_printout += str((weather_dict.values())) + "\n"
        # shows content of argument list
        weather_printout += str(args) + "\n"

        return weather_printout

    # specified output (quiet/verbose)
    if args.temperature:
        if args.Human:
            weather_printout += (weather_dict['Lufttemperatur'].replace(' °C', '')) + "\n"
        else:
            weather_printout += "Lufttemperatur: " + (weather_dict['Lufttemperatur']) + "\n"

    if args.airpressure:
        if args.Human:
            weather_printout += (weather_dict['Luftdruck (92 m ü.N.N.)'].replace(' hPa', '')) + "\n"
        else:
            weather_printout += "Luftdruck (92 m ü.N.N.): " + (weather_dict['Luftdruck (92 m ü.N.N.)']) + "\n"

    if args.humidity:
        if args.Human:
            weather_printout += (weather_dict['relative Feuchte'].replace(' %', '')) + "\n"
        else:
            weather_printout += "Luftfeuchtigkeit: " + (weather_dict['relative Feuchte']) + "\n"

    if args.power:
        if args.Human:
            weather_printout += (weather_dict['Windstärke'].replace(' Bf', '')) + "\n"
        else:
            weather_printout += "Windstaerke Bf: " + (weather_dict['Windstärke']) + "\n"

    if args.direction:
        if args.Human:
            weather_printout += (weather_dict['Windrichtung'].replace(' Grad', '')) + "\n"
        else:
            weather_printout += "Windrichtung: " + (weather_dict['Windrichtung']) + "\n"

    if args.velocity:
        if args.Human:
            str_tmp = weather_dict['Windstärke'].replace(' Bf', '')
            ms_tmp = bf_to_ms(int(str_tmp))
            str_rounded = str(round(ms_tmp, 2))
            weather_printout += str_rounded + "\n"

        else:
            str_tmp = weather_dict['Windstärke'].replace(' Bf', '')
            ms_tmp = bf_to_ms(int(str_tmp))
            weather_printout += "Windgeschwindigkeit m/s: " \
                                + str(round(ms_tmp, 2)) \
                                + " m/s" \
                                + "\n"

    if args.speed:
        if args.Human:
            str_tmp = weather_dict['Windstärke'].replace(' Bf', '')
            kmh_tmp = bf_to_ms(int(str_tmp)) * 3.6
            str_rounded = str(round(kmh_tmp, 2))
            weather_printout += str_rounded + "\n"

        else:
            str_tmp = weather_dict['Windstärke'].replace(' Bf', '')
            kmh_tmp = bf_to_ms(int(str_tmp)) * 3.6
            weather_printout += "Windgeschwindigkeit km/h: " \
                                + str(round(kmh_tmp, 2)) \
                                + " km/h" \
                                + "\n"

    return weather_printout


# data output in order of command line arguments
def value_to_string_order(args, weather_dict, request, order_str):  # returns string
    weather_printout = ""

    # specified output (quiet/verbose)
    for i in range(0, len(order_str)):
        if order_str[i] == 't':
            if args.temperature:
                if args.Human:
                    weather_printout += (weather_dict['Lufttemperatur'].replace(' °C', '')) + "\n"
                else:
                    weather_printout += "Lufttemperatur: " + (weather_dict['Lufttemperatur']) + "\n"
        elif order_str[i] == 'p':
            if args.airpressure:
                if args.Human:
                    weather_printout += (weather_dict['Luftdruck (92 m ü.N.N.)'].replace(' hPa', '')) + "\n"
                else:
                    weather_printout += "Luftdruck (92 m ü.N.N.): " + (
                        weather_dict['Luftdruck (92 m ü.N.N.)']) + "\n"
        elif order_str[i] == 'u':
            if args.humidity:
                if args.Human:
                    weather_printout += (weather_dict['relative Feuchte'].replace(' %', '')) + "\n"
                else:
                    weather_printout += "Luftfeuchtigkeit: " + (weather_dict['relative Feuchte']) + "\n"
        elif order_str[i] == 'w':
            if args.power:
                if args.Human:
                    weather_printout += (weather_dict['Windstärke'].replace(' Bf', '')) + "\n"
                else:
                    weather_printout += "Windstaerke Bf: " + (weather_dict['Windstärke']) + "\n"
        elif order_str[i] == 'd':
            if args.direction:
                if args.Human:
                    weather_printout += (weather_dict['Windrichtung'].replace(' Grad', '')) + "\n"
                else:
                    weather_printout += "Windrichtung: " + (weather_dict['Windrichtung']) + "\n"
        elif order_str[i] == 'v':
            if args.velocity:
                if args.Human:
                    str_tmp = weather_dict['Windstärke'].replace(' Bf', '')
                    ms_tmp = bf_to_ms(int(str_tmp))
                    str_rounded = str(round(ms_tmp, 2))
                    weather_printout += str_rounded + "\n"

                else:
                    str_tmp = weather_dict['Windstärke'].replace(' Bf', '')
                    ms_tmp = bf_to_ms(int(str_tmp))
                    weather_printout += "Windgeschwindigkeit m/s: " \
                                        + str(round(ms_tmp, 2)) \
                                        + " m/s" \
                                        + "\n"
        elif order_str[i] == 's':
            if args.speed:
                if args.Human:
                    str_tmp = weather_dict['Windstärke'].replace(' Bf', '')
                    kmh_tmp = bf_to_ms(int(str_tmp)) * 3.6
                    str_rounded = str(round(kmh_tmp, 2))
                    weather_printout += str_rounded + "\n"

                else:
                    str_tmp = weather_dict['Windstärke'].replace(' Bf', '')
                    kmh_tmp = bf_to_ms(int(str_tmp)) * 3.6
                    weather_printout += "Windgeschwindigkeit km/h: " \
                                        + str(round(kmh_tmp, 2)) \
                                        + " km/h" \
                                        + "\n"
        else:
            continue

    return weather_printout


def config_args(args):
    # Turns on --inverse flag if only data params are specified
    # to still allow inclusive-specified output.

    # If no args are given; every param is set to false (by default).
    # Below tests for that and then sets --inverse flag true,
    # therefore setting all data params true and printing all that.
    if (not args.temperature
            and not args.airpressure
            and not args.humidity
            and not args.power
            and not args.direction
            and not args.velocity
            and not args.speed
            and not args.debug
            and not args.inverse):
        args.inverse = True

    if args.inverse:
        args.temperature = not args.temperature
        args.airpressure = not args.airpressure
        args.humidity = not args.humidity
        args.direction = not args.direction
        args.velocity = not args.velocity
        args.power = not args.power
        args.speed = not args.speed


# Beaufort to metres/second converter
def bf_to_ms(bf_int):
    return 0.8360 * pow(bf_int, 3. / 2.)


if __name__ == "__main__":
    ret = main()
    print(ret, end='')
