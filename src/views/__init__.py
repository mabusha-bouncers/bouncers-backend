from typing import Optional

from flask_apispec import MethodResource
from flask_restful import Resource


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
