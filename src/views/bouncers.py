"""
**bouncers view**
"""
from typing import Generator, List

from flask import jsonify
from google.cloud import ndb

from src.cache import app_cache
from src.exceptions import InputError, DataServiceError
from src.utils.utils import return_ttl
from src.views import ViewModel, ListView
from src.models.users import BouncerModel


class BouncerView(ViewModel):
    """this view will handle bouncers API endpoints"""
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    method_decorators = []

    # TODO do not forget to add middlewares here
    def __init__(self):
        super(BouncerView, self).__init__()

    @staticmethod
    def get(uid: str):
        """
            will retrieve a single Bouncer by id
        :param uid:
        :return:
        """
        bouncer_instance: BouncerModel = BouncerModel.query(BouncerModel.uid == uid).get()
        if not isinstance(bouncer_instance, BouncerModel) or not bool(bouncer_instance):
            return jsonify(dict(status=False, message='unable to find bouncer with that id'))
        return jsonify(status=True, payload=bouncer_instance.to_dict(), message='bouncer successfully retrieved'), 200

    @staticmethod
    def post(bouncer_details: dict):
        """
            will create a bouncer from bouncer_details
        :param bouncer_details:
        :return:
        """
        # NOTE: bouncer uid should be supplied by the front end as part the login process
        # will use firebase for login
        uid: str = bouncer_details.get('uid')
        bouncer_instance: BouncerModel = BouncerModel.query(BouncerModel.uid == uid).get()
        if isinstance(bouncer_instance, BouncerModel) and bool(bouncer_instance):
            raise DataServiceError(description='You Already have an account')

        bouncer_instance: BouncerModel = BouncerModel(**bouncer_details)
        key: ndb.Key = bouncer_instance.put()
        if not isinstance(key, ndb.Key):
            _message: str = 'Unable to create new User due to a technical error please try again later'
            raise DataServiceError(description=_message)

        return jsonify(status=True, payload=bouncer_instance.to_dict(), message='successfully created new bouncer')

    @staticmethod
    def put(bouncer_details: dict):
        """
            will update a bouncer depending on bouncer details
        :param bouncer_details:
        :return:
        """
        uid: str = bouncer_details.get('uid')
        bouncer_instance: BouncerModel = BouncerModel.query(BouncerModel.uid == uid).get()
        if not isinstance(bouncer_instance, BouncerModel) or not bool(bouncer_instance):
            raise DataServiceError(description='Unable to find an account with that id please create a new account')

        bouncer_instance = BouncerModel(**bouncer_instance.to_dict(), **bouncer_details)
        key: ndb.Key = bouncer_instance.put()
        if not isinstance(key, ndb.Key):
            _message: str = 'Database Error: Unable to update user, please try again later'
            raise DataServiceError(description=_message)

        return jsonify(status=True, payload=bouncer_instance.to_dict(), message='successfully updated user details')

    @staticmethod
    def delete(uid: str):
        """
            will remove a bouncer from the database
        :param uid:
        :return:
        """
        if not isinstance(uid, str):
            raise InputError(description='uid must be an integer')

        bouncer_instance: BouncerModel = BouncerModel.query(BouncerModel.uid == uid).get()
        if not isinstance(bouncer_instance, BouncerModel) or not bool(bouncer_instance):
            raise DataServiceError(description='Unable to find an account with that id please create a new account')

        bouncer_instance.key.delete()

        return jsonify(status=True, message='user successfully deleted')


class BouncerListView(ListView):
    """
        **Class BouncerListView**        
            this view allows to users to get access to a total list of bouncers
    """
    methods = ['GET']

    def __init__(self):
        super(BouncerListView, self).__init__()

    def get(self):
        """
            returns a list of bouncers
        :return:
        """
        return jsonify(status=True, payload=self.bouncers_generator(), message='successfully retrieved bouncers')


class BouncersPageView(ListView):
    """
        **BouncersPageView**
            allows access to bouncers by pages of ten each time , however the page size can be modified
    """
    methods = ['GET', 'POST']

    def __init__(self):
        super(BouncersPageView, self).__init__()

    def get(self, page_number: int):
        """

        :param page_number:
        :return:
        """
        if not isinstance(page_number, int):
            raise InputError(description='page number should be an integer')

        return jsonify(status=True,
                       payload=self.bouncers_generator()[self.page_size * page_number:self.page_size],
                       message='successfully retrieved bouncers at that page')

