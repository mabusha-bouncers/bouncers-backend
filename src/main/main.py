"""
    Bouncers & Security Guards Dispatcher
        Web Application
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from src.config import config_instance
from flask import Flask
from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from src.cache import app_cache


def create_app(config=config_instance) -> Flask:
    """
    Battle Hall, War Room , Garrison Hall, Vehicle Factory, Class Barrack,  Barrack 1,

    Class APC Research , APC 1 Research & Vehicle Research


    **create_app**
        creates and initialize a Flask Application

    :param config: application configuration settings
    :return: Flask Application
    """
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        api = Api(app)
        app_cache.init_app(app=app)
        from src.views.bouncers import BouncerView, BouncersPageView, BouncerListView
        from src.views.clients import ClientView, ClientsPageView, ClientsListView

        api.add_resource(BouncerView, '/api/v1/bouncer', endpoint='get_update_bouncer',
                         methods=['GET', 'POST', 'PUT', 'DELETE'])
        api.add_resource(BouncersPageView, '/api/v1/bouncer/page', endpoint='get_bouncer_by_page',
                         methods=['GET'])
        api.add_resource(BouncerListView, '/api/v1/bouncer/list', endpoint='get_bouncers_list',
                         methods=['GET'])
        return app
