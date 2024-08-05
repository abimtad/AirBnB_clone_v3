#!/usr/bin/python3

""" A Flask Application """
from api.v1.views import app_views
from models import storage
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flasgger import Swagger
from flask_cors import CORS
from flasgger.utils import swag_from

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """ Close the Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error:
    ----------------
    responses:
      404:
        description: a resource was not found

    """
    return make_response(jsonify({'error': "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)

if __name__ == "__main__":
    """ The main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not port:
        port = '5000'
    if not host:
        host = '0.0.0.0'

    app.run(host=host, port=port, threaded=True)
