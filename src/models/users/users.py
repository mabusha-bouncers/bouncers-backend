"""
    user model this class controls user authentication meaning
        admin login and authorizations
        client login and authorization
        bouncers login and authorization
"""
from google.cloud import ndb
from datetime import date, datetime
from src.models.basemodel import BaseModel


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
    user_type: str = ndb.StringProperty()
    date_created: date = ndb.DateProperty(auto_now_add=True)
    last_login: datetime = ndb.DateTimeProperty(auto_now=True)

    def __bool__(self) -> bool:
        return bool(self.uid)

    def __str__(self) -> str:
        return f"<User: user_type: {self.user_type} " \
               f"names: {self.names}, surname: {self.surname}, email: {self.email}, cell: {self.cell}"
