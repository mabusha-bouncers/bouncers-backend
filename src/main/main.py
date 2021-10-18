from src.config import config_instance
from flask import Flask


def create_app(config=config_instance):
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        return app
