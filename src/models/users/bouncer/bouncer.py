"""
    Bouncers / Security Guards  Module
        module inherits from user and add bouncer specific functionality
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from google.cloud import ndb

from src.models.address import AddressModel
from src.models.users import UserModel


class BouncerModel(UserModel):
    """
        **BouncerModel**
            adds bouncer specific functionality to userModel

        **PARAMETERS**
            available: True if bouncer is available to go on duty
            contact_preference: cell / email -> defaults to cell phone
    """
    available: bool = ndb.BooleanProperty(default=False)
    certified: bool = ndb.BooleanProperty(default=False)
    security_grade: str = ndb.StringProperty(default=None)
    years_experience: int = ndb.IntegerProperty(default=0)
    rating: int = ndb.IntegerProperty(default=0)

    def __str__(self) -> str:
        return f"{super().__str__()} available: {self.available},  contact_preference: {self.contact_preference}" \
               f"Grade: {self.security_grade}, Rating: {self.rating}"

    def __bool__(self) -> bool:
        return super().__bool__()
