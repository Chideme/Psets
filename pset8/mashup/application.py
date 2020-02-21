import os
import re
from flask import Flask, jsonify, render_template, request

from cs50 import SQL
from helpers import lookup, cleaner

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Render map"""
    return render_template("index.html")


@app.route("/articles")
def articles():
    """Look up articles for geo"""
     # Ensure parameters are present
    if not request.args.get("geo"):
        raise RuntimeError("missing geo")

    # store the geo location
    geo = request.args.get("geo")

    # lookup for articles

    articles = lookup(geo)

    return jsonify([article for article in articles][0:5])



@app.route("/search")
def search():
    """Search for places that match query"""
    #Ensure parameters are present
    if not request.args.get("q"):
        raise RuntimeError("missing q")

    # store q
    q = request.args.get("q")


    if q[0].isdigit(): #check if q is a postal code
        areas = db.execute("SELECT * FROM places WHERE postal_code LIKE :q",q=q + "%")
    #if q is not a postal code
    else:
        # split q
        ql = cleaner(q)

        if len(ql) == 1:
            areas = db.execute("SELECT * FROM places WHERE  place_name LIKE :q",q= ql[0])
        elif len(ql) == 2:
            if len(ql[1]) == 2:
                areas = db.execute("SELECT * FROM places WHERE place_name = :q OR admin_code1 = :z ",q=ql[0], z=ql[1])
            else:
                areas = db.execute("SELECT * FROM places WHERE place_name = :q AND admin_name1 = :z ",q=ql[0],z=ql[1])
        else:
            areas = db.execute("SELECT * FROM places WHERE place_name =:q AND admin_name1 = :z and country_code = :p ", q=ql[0],z=ql[1],p=ql[2])
    return jsonify([area for area in areas])

@app.route("/update")
def update():
    """Find up to 10 places within view"""

    # Ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # Ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # Explode southwest corner into two variables
    sw_lat, sw_lng = map(float, request.args.get("sw").split(","))

    # Explode northeast corner into two variables
    ne_lat, ne_lng = map(float, request.args.get("ne").split(","))

    # Find 10 cities within view, pseudorandomly chosen if more within view
    if sw_lng <= ne_lng:

        # Doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # Crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # Output places as JSON
    return jsonify(rows)
