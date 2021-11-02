"""
**bouncers view**
"""
from flask import jsonify
from google.cloud import ndb

from src.exceptions import InputError, DataServiceError
from src.views import ViewModel
from src.models.users import BouncerModel


class BouncersView(ViewModel):
    """this view will handle bouncers API endpoints"""
    # TODO do not forget to add middlewares here
    def __init__(self):
        super(BouncersView, self).__init__()

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



    def put(self, bouncer_details: dict):
        """
            will update a bouncer depending on bouncer details
        :param bouncer_details:
        :return:
        """
        pass

    def delete(self, uid: str):
        """
            will remove a bouncer from the database
        :param uid:
        :return:
        """
        pass
