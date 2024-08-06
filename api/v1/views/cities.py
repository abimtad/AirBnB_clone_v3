#!/usr/bin/python3

""" This are obj that handles all default RestFul API actions for cities """

from models import storage
from models.state import State
from api.v1.views import app_views
from models.city import City
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
def get_cities(state_id):
    """ Retrieve the list of cities objects of a specific -
    State
    """
    listCities = []

    st = storage.get(State, state_id)
    if not st:
        abort(404)

    for city in st.cities:
        listCities.append(city.to_dict())

    return jsonify(listCities)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def get_city(city_id):
    """ Retrieve a specific city based on an id """

    cty = storage.get(City, city_id)

    if not cty:
        abort(404)

    return jsonify(cty.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
def delete_city(city_id):
    """ Delete a city based on id """

    cty = storage.get(City, city_id)

    if not cty:
        abort(404)
    storage.delete(cty)

    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/city/post_city.yml', methods=['POST'])
def post_city(state_id):
    """ Create a City """

    st = storage.get(State, state_id)
    if not st:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    dt = request.get_json()
    inst = City(**dt)
    inst.state_id = st.id
    inst.save()
    return make_response(jsonify(inst.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
def put_city(city_id):
    """ Update a City """

    cty = storage.get(City, city_id)
    if not cty:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'state_id', 'created_at', 'updated_at']

    dt = request.get_json()

    for key, value in dt.items():
        if key not in ignore:
            setattr(cty, key, value)

    storage.save()

    return make_response(jsonify(cty.to_dict()), 200)
