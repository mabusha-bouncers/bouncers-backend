"""
    Address Model
    will hold physical address for users
        includes
         bouncers, admins, clients and also place of events
"""
from google.cloud import ndb
from src.models.basemodel import BaseModel


class AddressModel(BaseModel):
    """
        **Class AddressModel**
            holds addresses for clients, admins, bouncers and places where events will take place
            or where work is available
    """
    address_id: str = ndb.StringProperty()
    street: str = ndb.StringProperty()
    city_town: str = ndb.StringProperty()
    province: str = ndb.StringProperty()
    country: str = ndb.StringProperty()
    postal_code: str = ndb.StringProperty()