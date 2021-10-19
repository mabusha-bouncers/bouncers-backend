"""
    Time Sheets module allows
        for keeping track of time worked by each bouncer
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from datetime import date, datetime
from enum import Enum
from typing import List

from google.cloud import ndb
from google.cloud.ndb import DateTimeProperty

from src.config import config_instance
from src.models.basemodel import BaseModel
from src.models.mixins.mixins import AmountMixin


class DaysOfWeekType(Enum):
    """
    Enumerator for DaysOfWeek
    """
    sunday = 0
    monday = 1
    tuesday = 2
    wednesday = 3
    thursday = 4
    friday = 5
    saturday = 6

    @classmethod
    def types(cls) -> List:
        return list(DaysOfWeekType)

    @classmethod
    def values(cls) -> List[int]:
        return [_day.value for _day in cls.types()]


class TimeSheetModel(BaseModel):
    """
        **TimeSheetModel**
            keeps track of hours worked per bouncer / security guard

        `PARAMETERS`
            uid: unique user identifier
            today: calendar date for today or day worked
            time_on_duty: date -> the date the bouncer started work
            time_of_duty: date -> the date the bouncer went of duty
            time_worked_hours: integer -> total time worked in hours
            hourly_rate: int (money in rands) -> hourly rate for bouncer
    """
    uid: str = ndb.StringProperty(indexed=True)
    day_of_week: int = ndb.IntegerProperty(choices=DaysOfWeekType.values(), default=DaysOfWeekType.monday.value)
    today: date = ndb.DateProperty()
    time_on_duty: datetime = ndb.DateTimeProperty()
    time_of_duty: datetime = ndb.DateTimeProperty()
    time_worked_hours: int = ndb.IntegerProperty()
    hourly_rate: int = ndb.IntegerProperty()

    #   TODO add overtime rates

    def total_earned(self) -> AmountMixin:
        """
        **total_earned**
            will return amount earned in currency format
            see AmountMixin
        :return:
        """
        amount_cents = self.time_worked_hours * self.hourly_rate * 100
        return AmountMixin(amount_cents=amount_cents, currency=config_instance.CURRENCY)

    def __str__(self) -> str:
        return f"<TimeSheet: rate: {self.hourly_rate} time worked: {self.time_worked_hours} " \
               f"total_earned: {self.total_earned}"

    def __bool__(self) -> bool:
        """
            **__bool__**
                determines if the timesheet is valid
        :return: boolean -> True if Valid
        """
        return bool(self.uid)


if __name__ == '__main__':
    for day in DaysOfWeekType.types():
        print(day.name, day.value)