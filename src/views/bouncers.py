"""
**bouncers view**
"""
from typing import Generator, List
from flask import jsonify
from google.cloud import ndb
from src.exceptions import InputError, DataServiceError, status_codes
from src.models.users.bouncer.bouncer import BouncerFeedbackModel
from src.utils.utils import return_ttl, create_id
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
    def get(uid: str) -> tuple:
        """
            will retrieve a single Bouncer by id
        :param uid:
        :return:
        """
        bouncer_instance: BouncerModel = BouncerModel.query(BouncerModel.uid == uid).get()
        if not isinstance(bouncer_instance, BouncerModel) or not bool(bouncer_instance):
            return jsonify(dict(status=False, message='unable to find bouncer with that id')), status_codes.status_ok_code
        return jsonify(dict(status=True, 
                            payload=bouncer_instance.to_dict(), 
                            message='bouncer successfully retrieved')), status_codes.successfully_updated_code

    @staticmethod
    def post(bouncer_details: dict) -> tuple:
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

        return jsonify(dict(status=True, 
                            payload=bouncer_instance.to_dict(), 
                            message='successfully created new bouncer')), status_codes.successfully_updated_code

    @staticmethod
    def put(bouncer_details: dict) -> tuple:
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

        return jsonify(dict(status=True, 
                            payload=bouncer_instance.to_dict(), 
                            message='successfully updated user details')), status_codes.successfully_updated_code

    @staticmethod
    def delete(uid: str) -> tuple:
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

        return jsonify(dict(status=True, 
                            message='user successfully deleted')), status_codes.successfully_updated_code


class BouncerListView(ListView):
    """
        **Class BouncerListView**        
            this view allows to users to get access to a total list of bouncers
    """
    methods = ['GET']

    def __init__(self):
        super(BouncerListView, self).__init__()

    def get(self) -> tuple:
        """
            returns a list of bouncers
        :return:
        """
        return jsonify(dict(status=True, 
                            payload=self.bouncers_generator(), 
                            message='successfully retrieved bouncers')), status_codes.status_ok_code


class BouncersPageView(ListView):
    """
        **BouncersPageView**
            allows access to bouncers by pages of ten each time , however the page size can be modified
    """
    methods = ['GET', 'POST']

    def __init__(self):
        super(BouncersPageView, self).__init__()

    def get(self, page_number: int) -> tuple:
        """

        :param page_number:
        :return:
        """
        if not isinstance(page_number, int):
            raise InputError(description='page number should be an integer')

        return jsonify(dict(status=True,
                            payload=self.bouncers_generator()[self.page_size * page_number:self.page_size],
                            message='successfully retrieved bouncers at that page')), status_codes.status_ok_code


class BouncerFeedBackView(ViewModel):
    """
        ** CLass BouncerFeedBackView **
            enables Bouncers to create feedback for clients
            enables bouncers to retrieve their own feedback
    """
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def __init__(self) -> None:
        super(BouncerFeedBackView, self).__init__()

    @staticmethod
    def get(feedback_id: str) -> tuple:
        """
            returns a specific feedback by feedback_id
        :return:
        """

        feedback = BouncerFeedbackModel.query(BouncerFeedbackModel.feedback_id == feedback_id).get()
        if not isinstance(feedback, BouncerFeedbackModel) or not bool(feedback):
            return jsonify(dict(status=False,
                                message='feedback with that id not found')), status_codes.data_not_found_code

        return jsonify(dict(status=True,
                            payload=feedback.to_dict(),
                            message='feedback successfully retrieved')), status_codes.status_ok_code

    @staticmethod
    def post(feedback: dict) -> tuple:
        """
            will accept feedback as dictionary then create
        :param feedback:
        :return:
        """

        feedback_instance: BouncerFeedbackModel = BouncerFeedbackModel(**feedback, feedback_id=create_id())
        key: ndb.Key = feedback_instance.put()
        if isinstance(key, ndb.Key):
            raise DataServiceError(description='error creating feedback')

        return jsonify(dict(status=True,
                            payload=feedback_instance.to_dict(),
                            message='successfully created feedback')), status_codes.successfully_updated_code

    @staticmethod
    def put(feedback: dict) -> tuple:
        """
            update bouncer feedback
        :param feedback:
        :return:
        """
        feedback_id: str = feedback.get('feedback_id')
        feedback_instance: BouncerFeedbackModel = BouncerFeedbackModel.query(
            BouncerFeedbackModel.feedback_id == feedback_id).get()
        if not isinstance(feedback_instance, BouncerFeedbackModel) or not bool(feedback_instance):
            return jsonify(dict(status=False,
                                message='feedback not found cannot be updated')), status_codes.data_not_found_code

        feedback_instance.update(feedback)
        key: ndb.Key = feedback_instance.put()
        if not isinstance(key, ndb.Key):
            raise DataServiceError(description='error updating feedback')

        return jsonify(dict(status=True,
                            payload=feedback_instance.to_dict(),
                            message='successfully updated feedback')), status_codes.successfully_updated_code

    @staticmethod
    def delete(feedback_id: str) -> tuple:
        """
            delete feedback
        :param feedback_id:
        :return:
        """
        feedback_instance: BouncerFeedbackModel = BouncerFeedbackModel.query(
            BouncerFeedbackModel.feedback_id == feedback_id).get()

        if not isinstance(feedback_instance, BouncerFeedbackModel) or not bool(feedback_instance):
            return jsonify(dict(status=False,
                                message='feedback not found cannot be deleted')), status_codes.data_not_found_code

        return jsonify(dict(status=True,
                            message='feedback successfully deleted')), status_codes.successfully_updated_code


class BouncerFeedbackListView(ViewModel):
    """**BouncerFeedbackListView**
    allows access to a list of bouncers feedback"""
    methods = ['GET']

    def __init__(self):
        super(BouncerFeedbackListView, self).__init__()

    @staticmethod
    def get(self, bouncer_id: str) -> tuple:
        """returns a list of feedback related to this bouncer"""
        feedback_list: List[dict] = [feedback.to_dict()
                                     for feedback in BouncerFeedbackModel.query(BouncerFeedbackModel.bouncer_id == bouncer_id)]
        return jsonify(dict(status=True,
                            payload=feedback_list,
                            message='successfully retrieved feedback')), status_codes.status_ok_code
