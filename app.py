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

    API_KEY = os.environ['MAPPING_KEY']
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

    try:
        # Receive POST body and parse for values
        data = request.json

        if data.get('address'):
            raise Exception("Wrong payload value")
        else:
            lat = data.get('lat')
            long = data.get('long')
            timezone = data.get('timezone')
    except Exception as e:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

    geo = Geolocation(lat=lat, long=long)
    results = geo.geohash(lat, long)

    sql_statement = 'INSERT INTO "geolocation" (lat, long, geohash) VALUES (%s, %s, %s)'
    values = (lat, long, results)
    geo.persist(sql_statement, values)
        
    return jsonify(results)

@app.route('/api/geo/geocode', methods=['POST'])
def geocode(): 
    
    try:
        # Receive POST body and parse for values
        data = request.json

        if data.get('lat') or data.get('lat'):
            raise Exception("Wrong payload value")
        else:
            address = data.get('address')
            timezone = data.get('timezone')
    except Exception as e:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

    geo = Geolocation(address=address)
    results = geo.geocode(address)
    lat = results[0]
    long = results[1]

    sql_statement = 'INSERT INTO "geolocation" (lat, long, address) VALUES (%s, %s, %s)'
    values = (lat, long, results)
    geo.persist(sql_statement, values)

    return jsonify(results)

@app.route('/api/geo/revcode', methods=['POST'])
def revcode(): 

    try:
        # Receive POST body and parse for values
        data = request.json

        if data.get('address'):
            raise Exception("Wrong payload value")
        else:
            lat = data.get('lat')
            long = data.get('long')
            timezone = data.get('timezone')
    except Exception as e:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

    geo = Geolocation(lat=lat, long=long)
    results = geo.rev_geocode(lat, long)
    
    sql_statement = 'INSERT INTO "geolocation" (lat, long, address) VALUES (%s, %s, %s)'
    values = (lat, long, results)
    geo.persist(sql_statement, values)

    return jsonify(results)
