#!/usr/bin/python3

""" This Objects handle all default RestFul API actions for Amenities"""

from models.amenity import Amenity
from api.v1.views import app_views
from models import storage
from flasgger.utils import swag_from
from flask import abort, jsonify, make_response, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/all_amenities.yml')
def get_amenities():
    """ Retrieve a list of all amenities """

    all_amen = storage.all(Amenity).values()
    list_amen = []

    for amen in all_amen:
        list_amen.append(amen.to_dict())
    return jsonify(list_amen)


@app_views.route('/amenities/<amenity_id>/', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/amenity/get_amenity.yml', methods=['GET'])
def get_amenity(amenity_id):
    """ Retrieve amenity """

    amen = storage.get(Amenity, amenity_id)

    if not amen:
        abort(404)

    return jsonify(amen.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/amenity/delete_amenity.yml', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Deletes an amenity  Object """

    amen = storage.get(Amenity, amenity_id)

    if not amen:
        abort(404)

    storage.delete(amen)

    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/amenity/post_amenity.yml', methods=['POST'])
def post_amenity():
    """ Create amenity """

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    dt = request.get_json()
    inst = Amenity(**dt)
    inst.save()
    return make_response(jsonify(inst.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/amenity/put_amenity.yml', methods=['PUT'])
def put_amenity(amenity_id):
    """ Update an amenity """

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignr = ['id', 'created_at', 'updated_at']

    amen = storage.get(Amenity, amenity_id)

    if not amen:
        abort(404)

    dt = request.get_json()
    for k, v in dt.items():
        if k not in ignr:
            setattr(amen, k, v)

    storage.save()

    return make_response(jsonify(amen.to_dict()), 200)
