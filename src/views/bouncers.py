"""
**bouncers view**
"""
from flask import jsonify

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

    def post(self, bouncer_details: dict):
        """
            will create a bouncer from bouncer_details
        :param bouncer_details:
        :return:
        """
        pass

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
