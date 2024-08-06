#!/usr/bin/python3
""" Objects that handle all default RestFul """

from models.state import State
from models.place import Place
from models.city import City
from models import storage
from models.user import User
from models.amenity import Amenity
from api.v1.views import app_views
from flasgger.utils import swag_from
from flask import abort, jsonify, make_response, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def get_places(city_id):
    """ Retrieve list of all Place objects of a City """

    cty = storage.get(City, city_id)

    if not cty:
        abort(404)

    plc = [place.to_dict() for place in cty.plc]

    return jsonify(plc)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def get_place(place_id):
    """ Retrieve a Place object """

    plc = storage.get(Plc, place_id)

    if not plc:
        abort(404)

    return jsonify(plc.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    """ Delete a Place Object """

    plc = storage.get(Place, place_id)

    if not plc:
        abort(404)

    storage.delete(plc)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def post_place(city_id):
    """ Create a Place """

    cty = storage.get(City, city_id)

    if not cty:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    dt = request.get_json()
    usr = storage.get(User, dt['user_id'])

    if not usr:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    dt["city_id"] = city_id
    inst = Place(**dt)
    inst.save()
    return make_response(jsonify(inst.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def put_place(place_id):
    """
    Updates a Place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    dt = request.get_json()
    if not dt:
        abort(400, description="Not a JSON")

    ignr = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for k, v in dt.items():
        if k not in ignr:
            setattr(place, k, v)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
@swag_from('documentation/place/post_search.yml', methods=['POST'])
def places_search():
    """ Retrieve all Place obj of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    dt = request.get_json()

    if dt and len(dt):
        state = dt.get('states', None)
        cty = dt.get('cities', None)
        amenities = dt.get('amenities', None)

    if not dt or not len(dt) or (
            not state and
            not cty and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if state:
        state_obj = [storage.get(State, s_id) for s_id in state]
        for state in state_obj:
            if state:
                for cy in state.cty:
                    if cy:
                        for place in city.places:
                            list_places.append(place)

    if cty:
        city_obj = [storage.get(City, c_id) for c_id in cty]
        for cy in city_obj:
            if cy:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [plac for plac in list_places
                       if all([m in place.amenities
                               for m in amenities_obj])]

    places = []
    for q in list_places:
        c = q.to_dict()
        c.pop('amenities', None)
        places.append(c)

    return jsonify(places)
