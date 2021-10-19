"""
    Address Model
    will hold physical address for users
        includes
         bouncers, admins, clients and also place of events
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from google.cloud import ndb
from src.models.basemodel import BaseModel


class AddressModel(BaseModel):
    """
        **Class AddressModel**
            holds addresses for clients, admins, bouncers and places where events will take place
            or where work is available
    """
    address_id: str = ndb.StringProperty(indexed=True)
    street: str = ndb.StringProperty()
    city_town: str = ndb.StringProperty()
    province: str = ndb.StringProperty()
    country: str = ndb.StringProperty()
    postal_code: str = ndb.StringProperty()

    @property
    def address(self) -> str:
        return f"{self.street}, {self.city_town}, {self.province}, {self.country}, {self.postal_code}"

    def __str__(self) -> str:
        return f"<Address: {self.address}"

    def __bool__(self) -> bool:
        return bool(self.address_id)
