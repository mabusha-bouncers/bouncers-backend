"""
    Clients Model  / Customers
        extends userModel and add client specific data
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from datetime import date
from enum import Enum
from typing import List
from google.cloud import ndb

from src.models.basemodel import BaseModel
from src.models.mixins.mixins import FeedbackMixin
from src.models.users import UserModel


class ClientRatingTypes(Enum):
    """
        **Class ClientRatingTypes**
            allows bouncer's and security guards to leave a rating for the client
    """
    not_rated = 0
    poor = 1
    good = 2
    best = 3
    very_best = 4

    @classmethod
    def types(cls) -> List:
        return list(cls)

    @classmethod
    def values(cls) -> List[int]:
        return [_rating.value for _rating in cls.types()]


class ClientTypes(Enum):
    """
        **ClientTypes**
            Enum for types of clients used in the application
    """
    business = 'business'
    personal = 'personal'

    @classmethod
    def types(cls) -> List:
        return list(cls)

    @classmethod
    def values(cls) -> List[str]:
        return [_client.value for _client in cls.types()]


class ClientModel(UserModel):
    """
        **Clients Model**
            adds client specific functionality to UserModel

        `PARAMETERS`
            client_type: str -> the type of client either its business client or personal client
            business: str -> Business Name if business Client
            description: str -> detailed description of client
            notes: str -> Notes about the client
    """
    client_type: str = ndb.StringProperty(default=ClientTypes.personal.value, choices=ClientTypes.values(),
                                          indexed=True)
    business: str = ndb.StringProperty()
    description: str = ndb.StringProperty()
    notes: str = ndb.StringProperty()

    def __str__(self) -> str:
        return f"{super().__str__()} client_type: {self.client_type}, Notes: {self.notes}"

    def __bool__(self) -> bool:
        return super().__bool__()


class ClientFeedbackModel(FeedbackMixin):
    """
        **Class ClientFeedbackModel**
            allows bouncers & security to leave feedback after each job,
            feedback is then averaged and then an overall score is saved for the client
        `PARAMETERS`
            client_uid: str = (uid) user id of client
            bouncer_uid: str = (uid) user id of bouncer
            feedback: str = actual feedback if any
            rating: int = rating from 0 to 4 (zero bad and 4 being good)
            date_created: date = auto always has the date the feedback was left
            date_updated: date = if updated will carry the date of the last update
    """
    rating: int = ndb.IntegerProperty(default=ClientRatingTypes.not_rated.value, choices=ClientRatingTypes.values())

    @property
    def rating_in_words(self) -> str:
        """
            **rating_in_words**
                returns rating in words
        """
        return [_rating.name for _rating in ClientRatingTypes if _rating.value == self.rating][0]

    def __str__(self) -> str:
        return f"<ClientFeedback: rating: {self.rating_in_words}, feedback: {self.feedback}"

    def __bool__(self) -> bool:
        return super().__bool__()


if __name__ == '__main__':
    print(ClientTypes.types())
