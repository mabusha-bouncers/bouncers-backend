"""
    Bouncers / Security Guards  Module
        module inherits from user and add bouncer specific functionality
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from enum import Enum, auto, IntEnum
from typing import List
from google.cloud import ndb
from src.models.users import UserModel


class BouncerRatingTypes:
    """
        **Class BouncerRatingTypes**
            start rating system for bouncers
    """
    not_rated: int = 0
    beginner: int = 1
    experienced: int = 2
    seasoned: int = 3
    advanced: int = 4
    professional: int = 5

    @classmethod
    def types(cls) -> List[int]:
        return [cls.not_rated, cls.beginner, cls.experienced, cls.seasoned, cls.advanced, cls.professional]


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
    rating = ndb.IntegerProperty(default=BouncerRatingTypes.not_rated,  choices=BouncerRatingTypes.types())

    def __str__(self) -> str:
        return f"{super().__str__()} available: {self.available},  contact_preference: {self.contact_preference}" \
               f"Grade: {self.security_grade}, Rating: {self.rating}"

    def __bool__(self) -> bool:
        return super().__bool__()


if __name__ == '__main__':
    for star_rating in BouncerRatingTypes.types():
        print(star_rating)
    print(BouncerRatingTypes.beginner)
    print(type(BouncerRatingTypes.beginner))
