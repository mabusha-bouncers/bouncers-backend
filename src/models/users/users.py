"""
    user model this class controls user authentication meaning
        admin login and authorizations
        client login and authorization
        bouncers login and authorization
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from abc import abstractmethod
from datetime import date, datetime
from enum import Enum
from typing import List

from google.cloud import ndb

from src.models.address import AddressModel
from src.models.mixins.mixins import UserMixin


class ContactPrefTypes(Enum):
    """Contact Preferences Type"""
    cell = 'cell'
    email = 'email'

    @classmethod
    def types(cls) -> List:
        return list(cls)

    @classmethod
    def values(cls) -> List[str]:
        return [_pref.value for _pref in cls.types()]


class UserType(Enum):
    """**Class UserTypes
        types of the users to use the application
    """
    admin = 'admin'
    client = 'client'
    bouncer = 'bouncer'

    @classmethod
    def types(cls) -> List:
        return list(cls)

    @classmethod
    def values(cls) -> List[str]:
        return [_user.value for _user in cls.types()]


class UserModel(UserMixin):
    """
        **Class UserModel**
            User Authentication and Authorization
        `Parameters:`
            uid: authentication will be handled by firebase and uid passed into this class for authorization
            names: first and last name of the user
            surname: surname of the user
            email: users email address
            cell: users cell number
            user_type: type of user either its admins, clients, or bouncers
            date_created and last_login are auto fields will always hold valid dates
            contact_preference -: str
    """
    names: str = ndb.StringProperty(required=True, indexed=True)
    surname: str = ndb.StringProperty(required=True, indexed=True)
    cell: str = ndb.StringProperty(required=True, indexed=True)
    user_type = ndb.StringProperty(default=UserType.bouncer.value, choices=UserType.values(), indexed=True)
    date_created: date = ndb.DateProperty(auto_now_add=True, indexed=True)
    last_login: datetime = ndb.DateTimeProperty(auto_now=True, indexed=True)
    address_key: ndb.Key = ndb.KeyProperty(kind=AddressModel)
    contact_preference: str = ndb.StringProperty(default=ContactPrefTypes.cell.value, choices=ContactPrefTypes.values())

    @property
    def address(self) -> AddressModel:
        return self.ndb.Key(self.address_key).get()

    @abstractmethod
    def rating(self):
        """every user instance must implement the rating method"""
        raise NotImplementedError

    @abstractmethod
    def rating_in_words(self) -> str:
        """user instance must have a rating in words method"""
        raise NotImplementedError

    def __bool__(self) -> bool:
        """returns true if this is a valid user"""
        return super().__bool__()

    def __str__(self) -> str:
        """returns the user representation in string format"""
        return f"{super().__str__()} {self.user_type} " \
               f"names: {self.names}, surname: {self.surname}, email: {self.email}, cell: {self.cell}"


if __name__ == "__main__":
    print(UserType.types())
    print(ContactPrefTypes.types())
