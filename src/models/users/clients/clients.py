"""
    Clients Model  / Customers
        extends userModel and add client specific data
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from enum import Enum
from typing import List
from google.cloud import ndb

from src.models.basemodel import BaseModel
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


class ClientFeedbackModel(BaseModel):
    """
        **Class ClientFeedbackModel**
            allows bouncers & security to leave feedback after each job,
            feedback is then averaged and then an overall score is saved for the client
    """
    client_uid: str = ndb.StringProperty()
    bouncer_uid: str = ndb.StringProperty()
    feedback: str = ndb.StringProperty()
    rating: int = ndb.IntegerProperty(default=ClientRatingTypes.not_rated.value, choices=ClientRatingTypes.values())


if __name__ == '__main__':
    print(ClientTypes.types())
