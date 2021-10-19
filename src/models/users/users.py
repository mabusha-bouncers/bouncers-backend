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

from typing import List

from google.cloud import ndb
from datetime import date, datetime
from src.models.address import AddressModel
from src.models.basemodel import BaseModel


class ContactPrefTypes:
    cell: str = 'cell'
    email: str = 'email'

    @classmethod
    def types(cls) -> List[str]:
        return [cls.cell, cls.email]


class UserType:
    admin = 'admin'
    client = 'client'
    bouncer = 'bouncer'

    @classmethod
    def types(cls) -> List[str]:
        return [cls.admin, cls.client, cls.bouncer]


class UserModel(BaseModel):
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
    """
    uid: str = ndb.StringProperty(indexed=True)
    names: str = ndb.StringProperty()
    surname: str = ndb.StringProperty()
    email: str = ndb.StringProperty()
    cell: str = ndb.StringProperty()
    user_type = ndb.StringProperty(default=UserType.bouncer, choices=UserType.types())
    date_created: date = ndb.DateProperty(auto_now_add=True)
    last_login: datetime = ndb.DateTimeProperty(auto_now=True)
    address_key: ndb.Key = ndb.KeyProperty(kind=AddressModel)
    contact_preference: str = ndb.StringProperty(default=ContactPrefTypes.cell, choices=ContactPrefTypes.types())

    @property
    def address(self) -> AddressModel:
        return self.ndb.Key(self.address_key).get()

    def __bool__(self) -> bool:
        return bool(self.uid)

    def __str__(self) -> str:
        return f"<User: user_type: {self.user_type} " \
               f"names: {self.names}, surname: {self.surname}, email: {self.email}, cell: {self.cell}"


if __name__ == "__main__":
    print(UserType.types())
    print(ContactPrefTypes.types())
