"""
    **Wrapper to handle application and ndb context**
        Should be used everytime a method which access ndb databases is being created or updated
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"

import functools
import os
from typing import Callable

from google.cloud import ndb

from src.config import config_instance
from src.utils.utils import is_development

if is_development():
    # NOTE: Local development service key is saved on local drive
    credential_path = "C:\\gcp_credentials\\bouncers.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def get_client() -> ndb.Client:
    return ndb.Client(namespace="main", project=config_instance.PROJECT)


def use_context(func: Callable):
    """
        **use_context**
            will insert ndb context for working with ndb. Cloud Databases
        **NOTE**

            functions/ methods needs to be wrapped by this wrapper when they interact with the database somehow

    :param func: function to wrap
    :return: function wrapped with ndb.context 
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        ndb_client = get_client()
        with ndb_client.context():
            return func(*args, **kwargs)
    return wrapper
