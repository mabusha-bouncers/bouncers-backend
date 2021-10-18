"""
    user model this class controls user authentication meaning
        admin login and authorizations
        client login and authorization
        bouncers login and authorization
"""
from google.cloud import ndb

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

    """
    uid: str = ndb.StringProperty(indexed=True)
    names: str = ndb.StringProperty()
    surname: str = ndb.StringProperty()
    email: str = ndb.StringProperty()
    cell: str = ndb.StringProperty()
    user_type: str = ndb.StringProperty()
