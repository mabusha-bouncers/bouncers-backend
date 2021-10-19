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


def create_app(config=config_instance):
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        return app
