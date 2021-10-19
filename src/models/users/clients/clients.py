"""
    Clients Model  / Customers
        extends userModel and add client specific data
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from typing import List
from google.cloud import ndb

from src.models.address import AddressModel
from src.models.users import UserModel


class ClientTypes:
    business: str = 'business'
    personal: str = 'personal'

    @classmethod
    def types(cls) -> List[str]:
        return [cls.business, cls.personal]


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
    client_type = ndb.StringProperty(choices=ClientTypes.types())
    business: str = ndb.StringProperty()
    description: str = ndb.StringProperty()
    notes: str = ndb.StringProperty()

    def __str__(self) -> str:
        return f"{super().__str__()} client_type: {self.client_type}, Notes: {self.notes}"

    def __bool__(self) -> bool:
        return super().__bool__()


if __name__ == '__main__':
    print(ClientTypes.types())