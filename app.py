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
    thoroughfare = None
    locality = None
    administrative_area = None
    sub_administrative_area = None
    country = None
    postal_code = None

    def __init__(self, lat, long):

        self.lat = lat
        self.long = long

    def geohash(self, lat, long):

        pass
    
    def geocode(self, address):

        geocode_result = self.gmaps.geocode(str(address))
        return geocode_result

    def rev_geocode(self, lat, long):

        rev_geocode_result = self.gmaps.reverse_geocode((lat, long))

        street_number = rev_geocode_result[0]['address_components'][0]['long_name']
        route = rev_geocode_result[0]['address_components'][1]['long_name']
        thoroughfare = street_number + route
        locality = rev_geocode_result[0]['address_components'][3]['long_name']
        administrative_area = rev_geocode_result[0]['address_components'][6]['short_name']
        sub_administrative_area = rev_geocode_result[0]['address_components'][5]['long_name']
        country = rev_geocode_result[0]['address_components'][7]['short_name']
        postal_code = rev_geocode_result[0]['address_components'][8]['long_name']

        return rev_geocode_result

    def persist(self, sql_statement):

        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(sql_statement)
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

    sql_statement = 'INSERT INTO "geolocation" (lat, long, geohash, country, administrative_area, sub_administrative_area, locality, \
        thoroughfare, postal_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (lat, long, geohash, geo.country, geo.administrative_area, geo.sub_administrative_area, geo.locality, geo.thoroughfare, geo.postal_code)
    geo.persist(sql_statement)

    return jsonify(results)