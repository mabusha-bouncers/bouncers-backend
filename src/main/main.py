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

docs = FlaskApiSpec()


def create_app(config=config_instance) -> Flask:
    """
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
        from src.views.bouncers import BouncerFeedBackView, BouncerFeedbackListView
        from src.views.clients import ClientView, ClientsPageView, ClientsListView
        from src.views.payments import PaymentView, PaymentListView

        # bouncers endpoints
        api.add_resource(BouncerView, '/api/v1/bouncer', endpoint='get_update_bouncer',
                         methods=['GET', 'POST', 'PUT', 'DELETE'])
        api.add_resource(BouncersPageView, '/api/v1/bouncer/page/<int:page_number>', endpoint='get_bouncer_by_page',
                         methods=['GET'])
        api.add_resource(BouncerListView, '/api/v1/bouncer/list', endpoint='get_bouncers_list',
                         methods=['GET'])

        # clients endpoints
        api.add_resource(ClientView, '/api/v1/client', endpoint='get_update_client',
                         methods=['GET', 'POST', 'PUT', 'DELETE'])
        api.add_resource(ClientsPageView, '/api/v1/client/page/<int:page_number>', endpoint='get_client_by_page',
                         methods=['GET'])
        api.add_resource(ClientsListView, '/api/v1/client/list', endpoint='get_client_list',
                         methods=['GET'])

        # bouncers feedback endpoints
        api.add_resource(BouncerFeedBackView, '/api/v1/bouncer/feedback/<string:feedback_id>',
                         endpoint='get_update_bouncer_feedback',
                         methods=['GET', 'PUT', 'DELETE'])

        api.add_resource(BouncerFeedBackView, '/api/v1/bouncer/feedback', endpoint='create_bouncer_feedback',
                         methods=['POST'])

        api.add_resource(BouncerFeedbackListView, '/api/v1/bouncer/feedback/list', endpoint='get_bouncer_feedback_list',
                         methods=['GET'])

        # payment endpoints
        api.add_resource(PaymentView, '/api/v1/payment/<string:payment_id>', endpoint='get_update_payment',
                         methods=['GET', 'PUT', 'DELETE'])
        api.add_resource(PaymentView, '/api/v1/payment', endpoint='create_payment',
                         methods=['POST'])

        api.add_resource(PaymentListView, '/api/v1/payment/list', endpoint='get_payment_list',
                         methods=['GET'])

        # swagger documentation

        app.config.update({
            'APISPEC_SPEC': APISpec(
                title='Bouncers API',
                version='0.0.1',
                plugins=[MarshmallowPlugin()],
                openapi_version='2.0.0'
            ),
            'APISPEC_SWAGGER_URL': '/api',
            'APISPEC_SWAGGER_UI_URL': '/api-ui'

        })
        # registering documentation
        docs.init_app(app)
        docs.register(target=BouncerView, endpoint='get_update_bouncer')
        docs.register(target=BouncersPageView, endpoint='get_bouncer_by_page')
        docs.register(target=BouncerListView, endpoint='get_bouncers_list')
        docs.register(target=ClientView, endpoint='get_update_client')
        docs.register(target=ClientsPageView, endpoint='get_client_by_page')
        docs.register(target=ClientsListView, endpoint='get_client_list')

        return app
