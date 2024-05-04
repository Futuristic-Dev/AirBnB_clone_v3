#!/usr/bin/python3
"""
Create an index model that holds the endpoint.
"""
from api.v1.views import app_views, storage
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Return the status of the API.
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    Return the number of each object by type.
    """
    models_available = {"User": "users",
                        "State": "states",
                        "City": "cities",
                        "Amenity": "amenities",
                        "Place": "places",
                        "Review": "reviews"}
    stats = {}
    for cls in models_available.keys():
        stats[models_available[cls]] = storage.count()
    return jsonify(stats)