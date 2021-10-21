"""
    Bouncers / Security Guards  Module
        module inherits from user and add bouncer specific functionality
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from datetime import date
from enum import Enum, auto, IntEnum
from statistics import mean
from typing import List
from google.cloud import ndb

from src.cache import app_cache
from src.models.basemodel import BaseModel
from src.models.context import get_client
from src.models.mixins.mixins import FeedbackMixin
from src.models.users import UserModel
from src.utils.utils import return_ttl


class BouncerRatingTypes(Enum):
    """
        **Class BouncerRatingTypes**
            start rating system for bouncers
    """
    not_rated = 0
    beginner = 1
    experienced = 2
    seasoned = 3
    advanced = 4
    professional = 5

    @classmethod
    def types(cls) -> List:
        return list(cls)

    @classmethod
    def values(cls) -> List[int]:
        return [rating.value for rating in cls.types()]


class SecurityGradesType(Enum):
    """
        **Class SecurityGradesType**
            PSIRA Security Gradc
    """
    grade_a = 'a'
    grade_b = 'b'
    grade_c = 'c'
    grade_d = 'd'
    grade_e = 'e'

    @classmethod
    def types(cls) -> List:
        return list(cls)

    @classmethod
    def values(cls) -> List[str]:
        return [_grade.value for _grade in cls.types()]


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
    security_grade: str = ndb.StringProperty(default=SecurityGradesType.grade_e.value,
                                             choices=SecurityGradesType.values())
    years_experience: int = ndb.IntegerProperty(default=0)

    @property
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def rating(self) -> int:
        """
            **rating**
                calculates average rating based on feedback left about the bouncer
        """
        with get_client().context():
            return int(mean([feedback.rating for feedback in BouncerFeedbackModel.query(
                BouncerFeedbackModel.bouncer_uid == self.uid)]))

    @property
    def rating_words(self) -> str:
        """bouncer rating in words"""
        return [_rating.name for _rating in BouncerRatingTypes.types() if _rating == self.rating][0]

    def __str__(self) -> str:
        return f"{super().__str__()} available: {self.available},  contact_preference: {self.contact_preference}" \
               f"Grade: {self.security_grade}, Rating: {self.rating_words}"

    def __bool__(self) -> bool:
        return super().__bool__()


class BouncerFeedbackModel(FeedbackMixin):
    """
        **BouncerFeedbackModel**
            allows clients to leave feedback about bouncers & security once the job
            is completed.

        `PARAMETERS`
    """
    rating: int = ndb.IntegerProperty(default=BouncerRatingTypes.not_rated.value, choices=BouncerRatingTypes.values())

    # noinspection PyPropertyDefinition
    @property
    def rating_in_words(self) -> str:
        return [_rating.name for _rating in BouncerRatingTypes.types() if _rating.value == self.rating][0]

    def __str__(self) -> str:
        return f"<BouncerFeedback: rating: {self.rating_in_words}, feedback: {self.feedback}"


if __name__ == '__main__':
    for star_rating in BouncerRatingTypes.types():
        print(star_rating, star_rating.value)

    print(BouncerRatingTypes.beginner)
    print(type(BouncerRatingTypes.beginner))
