#!/usr/bin/env python3
from flask import Flask, request, render_template
import urllib.request
import urllib.error
import configparser
import json

# Flask App
app = Flask(__name__, static_folder="static")
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = False

config_filename = "config.cfg"

config = configparser.ConfigParser()
config.read(config_filename)

api_key = config['Main']['GoogleAPIKey']

# Get
def osrm_exclude_request(start, end, transport_type):
    start_lat = start[0]
    start_lon = start[1]
    end_lat = end[0]
    end_lon = end[1]

    osrm_url = "http://127.0.0.1:5000/route/v1/{ttype}/{s_lon},{s_lat};{e_lon},{e_lat}?steps=true"\
        .format(ttype=transport_type, s_lon=start_lon, s_lat=start_lat, e_lon=end_lon, e_lat=end_lat)
    print(osrm_url)
    try:
        contents = urllib.request.urlopen(osrm_url).read()
    except urllib.error.HTTPError:
        contents = b'{"waypoints":[]}'
    print(contents)
    return contents

# Get
def osrm_normal_request(start, end, transport_type):
    start_lat = start[0]
    start_lon = start[1]
    end_lat = end[0]
    end_lon = end[1]

    osrm_url = "http://127.0.0.1:5001/route/v1/{ttype}/{s_lon},{s_lat};{e_lon},{e_lat}?steps=true"\
        .format(ttype=transport_type, s_lon=start_lon, s_lat=start_lat, e_lon=end_lon, e_lat=end_lat)
    print(osrm_url)
    try:
        contents = urllib.request.urlopen(osrm_url).read()
    except urllib.error.HTTPError:
        contents = b'{"waypoints":[]}'
    print(contents)
    return contents


# Disable caching!
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/")
def main():
    return render_template('index.html', google_api_key=api_key)

@app.route("/get_results")
def get_results():
    start = [float(request.args.get("start_lat")), float(request.args.get("start_lon"))]
    end = [float(request.args.get("end_lat")), float(request.args.get("end_lon"))]

    response_1 = osrm_exclude_request(start, end, "driving")
    response_2 = osrm_normal_request(start, end, "driving")

    resp_1_str = response_1.decode('UTF-8')
    resp_2_str = response_2.decode('UTF-8')

    exc = json.loads(resp_1_str)
    nor = json.loads(resp_2_str)

    len_exc = len(exc["waypoints"])
    len_nor = len(nor["waypoints"])

    response = "ERROR"

    if len_exc == 0 or len_exc > len_nor:
        response = "Recommended top take a car or bus."
    elif len_exc <= len_nor:
        response = "You can take an escooter, ebike, etc easily!"

    print("Len exc: " + str(len_exc) + " len nor: " + str(len_nor))

    return response


def run():
    app.run(host="0.0.0.0", port=80)

run()