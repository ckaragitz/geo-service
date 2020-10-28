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

class Geo:

    API_KEY = 'AIzaSyDEm_6KW_GQsex5wx9JiUADGajOFjYBAok'
    gmaps = googlemaps.Client(key=API_KEY)

    def __init__(self, lat, long, timezone, address):

        self.lat = lat
        self.long = long
        self.timezone = ''
        self.address = ''

    def geohash(self, lat, long):

        pass
    
    def geocode(self, lat, long, address):

        geocode_result = gmaps.geocode(str(address))
        return geocode_result

    def rev_geocode(self, lat, long):

        rev_geocode_result = gmaps.reverse_geocode((lat, long))
        return rev_geocode_result


@app.route('/api/geo/geohash', methods=['POST'])
def geohash(): 

    # Receive GET body and parse for values
    lat = request.args.get('lat')
    long = request.args.get('long')
    timezone = request.args.get('timezone')

    geolocation = Geo(lat, long)

    results = geolocation.geohash(lat, long)
    return jsonify(results)

@app.route('/api/geo/geocode', methods=['POST'])
def geocode(): 

    # Receive GET body and parse for values
    lat = request.args.get('lat')
    long = request.args.get('long')
    timezone = request.args.get('timezone')

    geolocation = Geo(lat, long)

    results = geolocation.geocode(lat, long)
    return jsonify(results)

@app.route('/api/geo/revcode', methods=['POST'])
def revcode(): 

    # Receive GET body and parse for values
    lat = request.args.get('lat')
    long = request.args.get('long')
    timezone = request.args.get('timezone')

    geolocation = Geo(lat, long)

    results = geolocation.rev_geocode(lat, long)
    return jsonify(results)