#!/usr/bin/python3

""" Index """

from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City
from models.user import User
from flask import jsonify  # type: ignore
from api.v1.views import app_views
from models import storage


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieve the number of each objects """
    clas = [City, Amenity, Place, Review, State, User]

    name = ["amenities",  "places", "cities", "reviews", "states", "users"]

    num_objs = {}

    for i in range(len(clas)):
        num_objs[name[i]] = storage.count(clas[i])

    return jsonify(num_objs)


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ The Status of an API """

    return jsonify({"status": "OK"})
