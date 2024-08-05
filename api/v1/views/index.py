#!/usr/bin/python3

""" An index """

from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City
from models.user import User
from models import storage
from flask import jsonify  # type: ignore
from api.v1.views import app_views


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieve the number of each objects by their type """
    classes = [City, Amenity, Place, Review, State, User]

    names = ["amenities",  "places", "cities", "reviews", "states", "users"]

    num_objs = {}

    for j in range(len(classes)):
        num_objs[names[j]] = storage.count(classes[j])

    return jsonify(num_objs)


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ The Status of the API """

    return jsonify({"status": "OK"})
