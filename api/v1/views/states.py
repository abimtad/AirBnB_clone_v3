#!/usr/bin/python3

""" Objects that handles all default-RestFul API actions """

from models.amenity import Amenity
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@swag_from('documentation/amenity/all_amenities.yml')
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieve a list of all amenities """
    all_amen = storage.all(Amenity).values()
    list_amen = []
    for amenity in all_amen:
        list_amen.append(amenity.to_dict())
    return jsonify(list_amen)


@app_views.route('/amenities/<amenity_id>/', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/amenity/get_amenity.yml', methods=['GET'])
def get_amenity(amenity_id):
    """ Retrieve amenity """
    amenty = storage.get(Amenity, amenity_id)
    if not amenty:
        abort(404)

    return jsonify(amenty.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/amenity/delete_amenity.yml', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Delete an amenity Obj """

    amen = storage.get(Amenity, amenity_id)

    if not amen:
        abort(404)

    storage.delete(amen)

    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/amenity/post_amenity.yml', methods=['POST'])
def post_amenity():
    """ Creates an amenity """

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    _data = request.get_json()
    instance = Amenity(**_data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/amenity/put_amenity.yml', methods=['PUT'])
def put_amenity(amenity_id):
    """ Updates an amenity """

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    amen = storage.get(Amenity, amenity_id)

    if not amen:
        abort(404)

    data = request.get_json()

    for k, v in data.items():
        if k not in ignore:
            setattr(amen, k, v)

    storage.save()

    return make_response(jsonify(amen.to_dict()), 200)
