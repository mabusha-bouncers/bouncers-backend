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

from enum import Enum
from typing import List

from google.cloud import ndb
from src.models.basemodel import BaseModel


class SAProvinceTypes(Enum):
    limpopo: str = 'limpopo'
    mpumalanga: str = 'mpumalanga'
    north_west: str = 'north_west'
    gauteng: str = 'gauteng'
    northern_cape: str = 'northern_cape'
    kwazulu_natal: str = 'kwazulu_natal'
    free_state: str = 'free_state'
    eastern_cape: str = 'eastern_cape'

    @classmethod
    def types(cls) -> List:
        return list(SAProvinceTypes)


class AddressModel(BaseModel):
    """
        **Class AddressModel**
            holds addresses for clients, admins, bouncers and places where events will take place
            or where work is available
    """
    address_id: str = ndb.StringProperty(indexed=True, required=True)
    street: str = ndb.StringProperty(indexed=True, required=True)
    city_town: str = ndb.StringProperty(indexed=True, required=True)
    province = ndb.StringProperty(choices=SAProvinceTypes.types(), indexed=True, required=True)
    country: str = ndb.StringProperty(default='south africa', required=True)
    postal_code: str = ndb.StringProperty(indexed=True, required=True)

    @property
    def address(self) -> str:
        return f"{self.street}, {self.city_town}, {self.province}, {self.country}, {self.postal_code}"

    def __str__(self) -> str:
        return f"<Address: {self.address}"

    def __bool__(self) -> bool:
        return bool(self.address_id)


if __name__ == '__main__':
    for province in SAProvinceTypes:
        print(province)
