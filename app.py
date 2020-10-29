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
import pygeohash as pgh

app = Flask(__name__)

class Geolocation:

    API_KEY = 'AIzaSyDEm_6KW_GQsex5wx9JiUADGajOFjYBAok'
    gmaps = googlemaps.Client(key=API_KEY)

    DATABASE_URL = os.environ['DATABASE_URL']
    formatted_address = None

    def __init__(self, lat=None, long=None, address=None):

        self.lat = lat
        self.long = long
        self.address = address

    def geohash(self, lat, long):

        geohash = pgh.encode(lat, long)
        return geohash
    
    def geocode(self, address):

        geocode_result = self.gmaps.geocode(str(address))

        self.lat = geocode_result[0]['geometry']['location']['lat']
        self.long = geocode_result[0]['geometry']['location']['lng']

        latlng = (self.lat, self.long)

        return latlng

    def rev_geocode(self, lat, long):

        rev_geocode_result = self.gmaps.reverse_geocode((lat, long))

        #self.street_number = rev_geocode_result[0]['address_components'][0]['long_name']
        #self.route = rev_geocode_result[0]['address_components'][1]['long_name']
        #self.thoroughfare = self.street_number + self.route
        #self.locality = rev_geocode_result[0]['address_components'][3]['long_name']
        #self.administrative_area = rev_geocode_result[0]['address_components'][6]['short_name']
        #self.sub_administrative_area = rev_geocode_result[0]['address_components'][5]['long_name']
        #self.country = rev_geocode_result[0]['address_components'][7]['short_name']
        #self.postal_code = rev_geocode_result[0]['address_components'][8]['long_name']

        self.formatted_address = rev_geocode_result[0]['formatted_address']

        return self.formatted_address

    def persist(self, sql_statement, values):

        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(sql_statement, values)
        conn.commit()
        cur.close()

################## API RESOURCES #####################
@app.route('/api/geo/geohash', methods=['POST'])
def geohash(): 

    # Receive POST body and parse for values
    data = request.json
    lat = data.get('lat')
    long = data.get('long')
    timezone = data.get('timezone')

    geo = Geolocation(lat=lat, long=long)

    results = geo.geohash(lat, long)
    return jsonify(results)

@app.route('/api/geo/geocode', methods=['POST'])
def geocode(): 

    # Receive POST body and parse for values
    data = request.json
    address = data.get('address')
    timezone = data.get('timezone')

    geo = Geolocation(address)
    results = geo.geocode(address=address)
    lat = results[0]
    long = results[1]

    sql_statement = 'INSERT INTO "geolocation" (lat, long, address) VALUES (%s, %s, %s)'
    values = (lat, long, results)
    geo.persist(sql_statement, values)

    return jsonify(results)

@app.route('/api/geo/revcode', methods=['POST'])
def revcode(): 

        # Receive POST body and parse for values
        data = request.json
        lat = data.get('lat')
        long = data.get('long')
        timezone = data.get('timezone')

    geo = Geolocation(lat, long)
    results = geo.rev_geocode(lat=lat, long=long)

    #sql_statement = 'INSERT INTO "geolocation" (lat, long, country, administrative_area, sub_administrative_area, locality, \
        #thoroughfare, postal_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    #values = (lat, long, geo.country, geo.administrative_area, geo.sub_administrative_area, geo.locality, geo.thoroughfare, geo.postal_code)
    
    sql_statement = 'INSERT INTO "geolocation" (lat, long, address) VALUES (%s, %s, %s)'
    values = (lat, long, results)
    geo.persist(sql_statement, values)

    return jsonify(results)