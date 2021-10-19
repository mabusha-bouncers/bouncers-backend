"""
    Clients Model
        extends userModel and add client specific data
"""
from google.cloud import ndb
from src.models.users import UserModel


class ClientModel(UserModel):
    """
        **Clients Model**
            adds client specific functionality to UserModel
    """
    client_address: ndb.Key = ndb.KeyProperty()


