"""
**Clients API View
"""
from flask import jsonify

from src.exceptions import DataServiceError, status_codes
from src.views import ViewModel
from src.models.users.clients import ClientModel


class ClientView(ViewModel):
    """**Client View**
        allows access to methods to
            get, create and update Client Details
    """
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def __init__(self):
        super(ClientView, self).__init__()

    @staticmethod
    def get(uid: str):
        """
            returns a specific client
        :param uid:
        :return:
        """
        client_instance: ClientModel = ClientModel.query(ClientModel.uid == uid).first()
        if not isinstance(client_instance, ClientModel) or not bool(client_instance):
            raise DataServiceError(description='A Client with that ID does not exist please create a new account')

        _message: str = 'successfully fetched client details'
        return jsonify(dict(status=True,
                            payload=client_instance.to_dict(),
                            message=_message)), status_codes.status_ok_code
