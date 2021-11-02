"""
**Clients API View
"""
from flask import jsonify
from google.cloud import ndb

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
        client_instance: ClientModel = ClientModel.query(ClientModel.uid == uid).get()
        if not isinstance(client_instance, ClientModel) or not bool(client_instance):
            raise DataServiceError(description='A Client with that ID does not exist please create a new account')

        _message: str = 'successfully fetched client details'
        return jsonify(dict(status=True,
                            payload=client_instance.to_dict(),
                            message=_message)), status_codes.status_ok_code

    @staticmethod
    def post(client_details: dict):
        """

        :param client_details:
        :return:
        """
        uid: str = client_details.get('uid')
        client_instance: ClientModel = ClientModel.query(ClientModel.uid == uid).get()
        if isinstance(client_instance, ClientModel) and bool(client_instance):
            raise DataServiceError(description='A Client with that ID already exist')
        
        client_instance: ClientModel = ClientModel(**client_details)

        _message: str = 'successfully created client'
        return jsonify(dict(status=True,
                            payload=client_instance.to_dict(),
                            message=_message)), status_codes.status_ok_code

    @staticmethod
    def put(client_details: dict):
        """
            update client details
        :param client_details:
        :return:
        """
        uid: str = client_details.get('uid')
        client_instance: ClientModel = ClientModel.query(ClientModel.uid == uid).get()
        if not isinstance(client_instance, ClientModel) or not bool(client_instance):
            raise DataServiceError(description='A Client with that ID does not exist')

        # TODO - limit the properties that to_dict() returns here
        client_instance: ClientModel = ClientModel(**client_instance.to_dict(), **client_details)
        key: ndb.Key = client_instance.put()
        if not isinstance(key, ndb.Key):
            raise DataServiceError(description='Unable to update client details')
        _message: str = 'successfully updated client'
        return jsonify(dict(status=True,
                            payload=client_instance.to_dict(),
                            message=_message)), status_codes.status_ok_code



