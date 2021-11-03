"""
**Clients API View
"""
from flask import jsonify
from google.cloud import ndb

from src.exceptions import DataServiceError, status_codes
from src.views import ViewModel, ListView
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
        **get**
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
        **post**
            create a client instance from client details
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
        **put**
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

    @staticmethod
    def delete(uid: str):
        """
            **delete*
                delete client details from database
        :param uid:
        :return:
        """
        client_instance: ClientModel = ClientModel.query(ClientModel.uid == uid).get()
        if isinstance(client_instance, ClientModel):
            client_instance.key.delete()
            return jsonify(dict(status=True,
                                message='client successfully deleted')), status_codes.successfully_updated_code
        return jsonify(dict(status=False,
                            message='client does not exist may already have been deleted')), status_codes.data_not_found_code


class ClientsListView(ListView):
    """
        **Class ClientsListView**
            enables retrieval of full client lists
    """
    def __init__(self):
        super(ClientsListView, self).__init__()

    def get(self):
        return jsonify(dict(status=True,
                            payload=self.client_generator(),
                            message='successfully retrieved client list')), status_codes.status_ok_code


class ClientsPageView(ListView):
    """
        enables the retrieval of clients by page number
    """
    def __init__(self):
        super(ClientsPageView, self).__init__()

    def get(self, page_number: int):
        """

        :param page_number:
        :return:
        """
        return jsonify(dict(status=True,
                            payload=self.client_generator()[self.page_size * page_number: self.page_size],
                            message='successfully retrieved clients')), status_codes.status_ok_code
