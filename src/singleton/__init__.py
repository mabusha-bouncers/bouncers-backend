"""
    **Class Singleton**
        enables definitions of singleton classes by inheriting this class
"""


class Singleton(type):
    """
        **Class Singleton**
            singleton instance
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    