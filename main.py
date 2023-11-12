import materiel
import route
import degradation
import rapportNiveau
import json
import re
from flask import Flask
from flask import render_template
from flask import request
from route import Route

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    road = None
    coord = [None, None, None]
    listes = Route.get_degraded_route()
    if request.method == 'POST':
        road = Route.get_route(request.form['idRoute'])
        degraded_points = road.get_center_degraded_point()
        coord = road.get_route_coordinate()
    return render_template("index.html", listes = listes, road = road, latitude = coord[0], longitude = coord[1], geoJSON = coord[2], degraded_points = degraded_points, degats = road.get_degradations(), nb_detruit= len(degraded_points))