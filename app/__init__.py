from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from app.common.database import Database
from app.common.response import Response
from config import config


def create_app(config_name):
    app = Flask(__name__)
    api = Api(app)
    jwt = JWTManager(app)
    app.config.from_object(config[config_name])
    # Register our blueprints
    from .default import default as default_blueprint
    app.register_blueprint(default_blueprint)


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    @app.before_first_request
    def init_db():
        Database.initialize()

    return app
