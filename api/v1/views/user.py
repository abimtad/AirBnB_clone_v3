#!/usr/bin/python3

""" Objects that handle all default RestFul API actions for Users """

from models import storage
from models.user import User
from api.v1.views import app_views
from flasgger.utils import swag_from
from flask import abort, jsonify, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    """ Retrieve list user objects - """

    allUsers = storage.all(User).values()

    listUsers = []

    for user in allUsers:
        listUsers.append(user.to_dict())
    return jsonify(listUsers)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    """ Retrieve an user """

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """ Delete a user Object """

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)

    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])
def post_user():
    """ Creates a user """

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")

    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    dt = request.get_json()
    inst = User(**dt)
    inst.save()
    return make_response(jsonify(inst.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def put_user(user_id):
    """ Updates a user """

    usr = storage.get(User, user_id)

    if not usr:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignr = ['id', 'email', 'created_at', 'updated_at']

    dt = request.get_json()
    for k, v in dt.items():
        if k not in ignr:
            setattr(usr, k, v)

    storage.save()

    return make_response(jsonify(usr.to_dict()), 200)
