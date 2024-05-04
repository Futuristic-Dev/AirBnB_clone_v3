#!/usr/bin/python3
"""
Create a module that contains the logic of amenities.
"""

from api.v1.views import (app_views, Amenity, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('amenties/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenities(amenity_id=None):
    """
    Return the list of all amenities or a specific amenity.
    """
    if amenity_id is None:
        all_amenities = [state.to_json() for state in storage.all
                         ("Amenity").values()]
        return jsonify(all_amenities)
    store = storage.get("Amenity", amenity_id)
    if store is None:
        abort(404)
    return jsonify(store.to_json())

@app_views.route('/amenties/<amentity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id=None):
    """
    Delete an amenity.
    """
    store = storage.get("Amenity", amenity_id)
    if store is None:
        abort(404)
    storage.delete(store)
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """
    Create an amenity.
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return jsonify(new_amenity.to_json()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """
    Update an amenity.
    """
    store = storage.get("Amenity", amenity_id)
    if store is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(store, key, value)
    store.save()
    return jsonify(store.to_json()), 200