"""
Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

from urllib.request import urlopen
import json


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urlopen(url)
    response_text = f.read()
    response_data = json.loads(str(response_text, "utf-8"))
    return response_data

def get_url(place_name):
    place_name = place_name.replace(" ", "+")
    url = GMAPS_BASE_URL + "?address=" + place_name
    return url

def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    url = get_url(place_name)
    j = get_json(url)
    coor = j['results']
    coor = coor[0]
    coor = coor['geometry']
    coor = coor['location']
    return coor


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    url = MBTA_BASE_URL + "?api_key=" + MBTA_DEMO_API_KEY +"&lat=" + str(latitude) + "&lon=" + str(longitude) + "&format=json"
    j = get_json(url)
    station = j['stop']
    station = station[0]
    distance = station['distance']
    station = station['parent_station_name']
    res = (station, distance)
    return res


def find_stop_near(place_name):
    """
    Given a place name or address, print the nearest MBTA stop and the
    distance from the given place to that stop.
    """
    latlong = get_lat_long(place_name)
    print(get_nearest_station(latlong['lat'],latlong['lng']))

find_stop_near('TD Garden')
