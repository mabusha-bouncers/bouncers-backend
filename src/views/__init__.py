from typing import Optional, List

from flask import jsonify

from src.cache import app_cache
from src.exceptions import InputError
from src.models.users import BouncerModel, ClientModel
from src.utils.utils import return_ttl


class ViewModel(MethodResource, Resource):
    """
    **ViewModel**
        base viewModel for all the API Views
    """
    methods = []
    method_decorators = []
    # TODO add authenticators and other middlewares here

    def __init__(self) -> None:
        super(ViewModel, self).__init__()


class ListView(ViewModel):
    """allows access to a list of bouncers"""
    default_page_size: int = 10
    methods = ['GET', 'POST']
    method_decorators = []

    def __init__(self):
        super(ListView, self).__init__()
        self.page_size: int = self.default_page_size

    @staticmethod
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def bouncers_generator() -> List[BouncerModel]:
        """this method will obtain and memoize the list of bouncers from the database"""
        return [bouncer.to_dict() for bouncer in BouncerModel.query()]

    @staticmethod
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def client_generator() -> List[ClientModel]:
        """

        :return:
        """
        return [client.to_dict() for client in ClientModel.query()]

    def post(self, page_size: int):
        """
        **post**
            update page size
        :param page_size:
        :return:
        """
        self.page_size = page_size
        if not isinstance(page_size, int) or page_size < self.default_page_size:
            raise InputError(description=f'Invalid Page size must be an integer not less than {self.default_page_size}')
        return jsonify(status=True, message=f'page size successfully set to {self.page_size}')
