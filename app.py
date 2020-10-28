from __future__ import print_function
from flask import Flask, request, jsonify
from datetime import datetime
import googlemaps
import json
import pprint
import requests
import sys
import urllib
import os
import json
import psycopg2

app = Flask(__name__)

class Geolocation:

    API_KEY = 'AIzaSyDEm_6KW_GQsex5wx9JiUADGajOFjYBAok'
    gmaps = googlemaps.Client(key=API_KEY)

    def __init__(self, lat, long):

        self.lat = lat
        self.long = long

    def geohash(self, lat, long):

        pass
    
    def geocode(self, lat, long, address):

        geocode_result = self.gmaps.geocode(str(address))
        return geocode_result

    def rev_geocode(self, lat, long):

        rev_geocode_result = self.gmaps.reverse_geocode((lat, long))
        return rev_geocode_result


@app.route('/api/geo/geohash', methods=['POST'])
def geohash(): 

    # Receive POST body and parse for values
    data = request.json
    lat = data.get('lat')
    long = data.get('long')
    timezone = data.get('timezone')

    geo = Geolocation(lat, long)

    results = geo.geohash(lat, long)
    return jsonify(results)

@app.route('/api/geo/geocode', methods=['POST'])
def geocode(): 

    # Receive POST body and parse for values
    data = request.json
    lat = data.get('lat')
    long = data.get('long')
    timezone = data.get('timezone')

    geo = Geolocation(lat, long)

    results = geo.geocode(lat, long)
    return jsonify(results)

@app.route('/api/geo/revcode', methods=['POST'])
def revcode(): 

    # Receive POST body and parse for values
    data = request.json
    lat = data.get('lat')
    long = data.get('long')
    timezone = data.get('timezone')

    geo = Geolocation(lat, long)

    results = geo.rev_geocode(lat, long)
    return jsonify(results)