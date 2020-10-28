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

    DATABASE_URL = os.environ['DATABASE_URL']

    def __init__(self, lat, long):

        self.lat = lat
        self.long = long

    def geohash(self, lat, long):

        pass
    
    def geocode(self, address):

        geocode_result = self.gmaps.geocode(str(address))
        return geocode_result

    def rev_geocode(self, lat, long):

        self.reverse = True

        rev_geocode_result = self.gmaps.reverse_geocode((lat, long))

        print(rev_geocode_result)
        print('\n')

        #street_number = rev_geocode_result.get('street_number')
        #route = rev_geocode_result.get('route')
        #thoroughfare = street_number + route
        #locality = rev_geocode_result.get('locality')
        #administrative_area = rev_geocode_result.get('administrative_area_level_1')
        #sub_administrative_area = rev_geocode_result.get('administrative_area_level_2')
        #country = rev_geocode_result.get('country')
        return rev_geocode_result

    def persist(self, lat, long, geohash = None, country = None, administrative_area = None, sub_administrative_area = None, locality = None, thoroughfare = None, postal_code = None):

        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        if self.reverse:
            # Insertion operations
            cur.execute('INSERT INTO "geolocation" (lat, long, geohash, country, administrative_area, sub_administrative_area, locality, \
            thoroughfare, postal_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (lat, long, geohash, country, administrative_area, sub_administrative_area, locality, thoroughfare, postal_code))
            conn.commit()
            cur.close()


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