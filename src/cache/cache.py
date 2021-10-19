"""
    Cache Manager for Bouncers & Security Guards Dispatcher
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from src.config import config_instance
from src.singleton import Singleton
from flask_caching import Cache


class CacheManager(Singleton):
    """
    **CacheManager**
            application specific cache manager

    """

    def __init__(self):
        self._cache: Cache = Cache(config=config_instance.cache_dict())

    def init_app(self, app):
        self._cache.init_app(app=app)

    @property
    def cache(self):
        return self._cache


app_cache: CacheManager = CacheManager()
