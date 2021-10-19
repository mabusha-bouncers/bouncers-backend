"""
    Cache Manager for Bouncers & Security Guards Dispatcher
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from src.singleton import Singleton


class CacheManager(Singleton):
    def __init__(self, app):
        pass


app_cache: CacheManager = CacheManager()
