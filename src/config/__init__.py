"""
    **Flask App Configuration Settings**
    *Python Version 3.8 and above*
    Used to setup environment variables for python flask app
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"

import os
import typing
# noinspection PyPackageRequirements
from decouple import config
from src.singleton import Singleton
import datetime


class Config(Singleton):
    """
        **APP Configuration Settings**
            configuration variables for setting up the application
    """

    # TODO - Clean up configuration settings
    def __init__(self) -> None:
        # APP URLS
        self.PROJECT: str = "bouncers"
        self.BASE_URL: str = os.environ.get("BASE_URL") or config("BASE_URL")

        self.ADMIN_UID: str = os.environ.get("ADMIN_UID") or config("ADMIN_UID")
        self.ADMIN_EMAIL: str = os.environ.get("ADMIN_EMAIL") or config("ADMIN_EMAIL")
        self.ADMIN_NAMES: str = os.environ.get("ADMIN_NAMES") or config("ADMIN_NAMES")
        self.ADMIN_SURNAME: str = os.environ.get("ADMIN_SURNAME") or config("ADMIN_SURNAME")
        self.ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD") or config("ADMIN_PASSWORD")
        self.ADMIN_CELL: str = os.environ.get("ADMIN_CELL") or config("ADMIN_CELL")

        self.UTC_OFFSET = datetime.timedelta(hours=2)
        self.DATASTORE_TIMEOUT: int = 360  # seconds 6 minutes
        self.DATASTORE_RETRIES: int = 3  # total retries when saving to datastore

        self.CURRENCY: str = "USD"

        self.IS_PRODUCTION: bool = True
        self.SECRET_KEY: str = os.environ.get("SECRET_KEY") or config("SECRET_KEY")
        self.DEBUG: bool = False

        self.CACHE_TYPE: str = "simple"
        self.CACHE_DEFAULT_TIMEOUT: int = 60 * 60 * 6
        self.MEM_CACHE_SERVER_URI: str = ""
        self.GOOGLE_APPLICATION_CREDENTIALS: str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        # NOTE : setting IS_PRODUCTION here - could find a better way of doing this rather
        # than depending on the OS
        if "DESKTOP-B52R0UU" == os.environ.get('COMPUTERNAME'):
            self.DEBUG = True
            self.IS_PRODUCTION = False
            self.ENV = "development"
            self.PROPAGATE_EXCEPTIONS: bool = True
            self.PRESERVE_CONTEXT_ON_EXCEPTION: bool = True
            self.EXPLAIN_TEMPLATE_LOADING: bool = False
            self.PREFERRED_URL_SCHEME: str = "http"
            self.TESTING: bool = True
            # TODO - set Cache to MEM_CACHE and then setup the server URI, applicable on version 2

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return self.__str__()

    def cache_dict(self) -> dict:
        """
            Consider converting the cache to MEM_CACHE Type or Redis
            preferably host the cache as a docker instance on Cloud Run
        :return: dict
        """
        # TODO : use redis cache here instead of simple cache
        return {
            "CACHE_TYPE": "simple",
            "CACHE_DEFAULT_TIMEOUT": self.CACHE_DEFAULT_TIMEOUT,
            "CACHE_KEY_PREFIX": "memberships_cache_"
        }


config_instance: Config = Config()
# Note: Config is a singleton - this means it cannot be redeclared anywhere else
del Config
