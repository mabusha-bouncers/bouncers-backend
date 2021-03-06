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
    limpopo = 'limpopo'
    mpumalanga = 'mpumalanga'
    north_west = 'north_west'
    gauteng = 'gauteng'
    northern_cape = 'northern_cape'
    kwazulu_natal = 'kwazulu_natal'
    free_state = 'free_state'
    eastern_cape = 'eastern_cape'
    western_cape = 'western_cape'

    @classmethod
    def types(cls) -> list:
        return list(cls)

    @classmethod
    def values(cls) -> List[str]:
        """
            returns values only from enumerated provinces
        """
        return [_item.value for _item in cls.types()]


class AddressModel(BaseModel):
    """
        **Class AddressModel**
            holds addresses for clients, admins, bouncers and places where events will take place
            or where work is available
        `PARAMETERS`
        
            address_id: 
    """
    address_id: str = ndb.StringProperty(indexed=True, required=True)
    street: str = ndb.StringProperty(indexed=True, required=True)
    city_town: str = ndb.StringProperty(indexed=True, required=True)
    province = ndb.StringProperty(default=SAProvinceTypes.gauteng.value, choices=SAProvinceTypes.values(), indexed=True,
                                  required=True)
    country: str = ndb.StringProperty(default='south africa', required=True)
    postal_code: str = ndb.StringProperty(indexed=True, required=True)

    @property
    def address(self) -> str:
        """**address**
         returns the address as string"""
        return f"{self.street}, {self.city_town}, {self.province}, {self.country}, {self.postal_code}"
    
    @property
    def address_dict(self) -> dict:
        """**address_dict**
        returns the address as dict"""
        return {
            'address_id': self.address_id,
            'street': self.street,
            'city_town': self.city_town,
            'province': self.province,
            'country': self.country,
            'postal_code': self.postal_code
        }

    def __str__(self) -> str:
        """returns address in string format"""
        return f"<Address: {self.address}"

    def __bool__(self) -> bool:
        """returns true if address is valid"""
        return bool(self.address_id)


if __name__ == '__main__':
    for province in SAProvinceTypes.types():
        print(province)
