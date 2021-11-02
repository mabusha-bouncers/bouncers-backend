"""
**bouncers view**
"""
from src.views import ViewModel


class BouncersView(ViewModel):
    """this view will handle bouncers API endpoints"""

    def get(self, uid: str):
        """
            will retrieve a single Bouncer by id
        :param uid:
        :return:
        """
        pass

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