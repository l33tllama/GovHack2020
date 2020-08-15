#!/usr/bin/env python3
from flask import Flask, request, render_template
import configparser

# Flask App
app = Flask(__name__, static_folder="static")
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = False

config_filename = "config.cfg"

config = configparser.ConfigParser()
config.read(config_filename)

api_key = config['Main']['GoogleAPIKey']

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


def run():
    app.run(host="0.0.0.0", port=80)

run()