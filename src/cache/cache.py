from src.singleton import Singleton


class CacheManager(Singleton):
    def __init__(self, app):
        pass


app_cache: CacheManager = CacheManager()
