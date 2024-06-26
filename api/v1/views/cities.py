#!/usr/bin/python3
"""
Create a module that contains the logic of cities.
"""

from api.v1.views import (app_views, City, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """
    Return the list of all cities in a state.
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = [city.to_json() for city in state.cities]
    return jsonify(cities)

@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """
    Return the city by id.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_json())

@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    Delete a city by id.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    return jsonify({}), 200

@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def post_city(state_id):
    """
    Create a city.
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_city = City(**request.get_json())
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_json()), 201

@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """
    Update a city.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_json()), 200