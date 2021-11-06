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

from src.config import config_instance
from src.models.basemodel import BaseModel
from src.models.mixins.mixins import AmountMixin


class DaysOfWeekType(Enum):
    """
        **DaysOfWeekType**
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
            and total pay for those hours

        `PARAMETERS`
            uid: unique user identifier
            today: calendar date for today or day worked
            time_on_duty: date -> the date the bouncer started work
            time_of_duty: date -> the date the bouncer went of duty
            time_worked_hours: integer -> total time worked in hours
            hourly_rate: int (money in rands) -> hourly rate for bouncer
            time_sheet_paid: bool -> False as default True when time worked has been paid
    """
    uid: str = ndb.StringProperty(indexed=True)
    timesheet_id: str = ndb.StringProperty(indexed=True)
    day_of_week: int = ndb.IntegerProperty(choices=DaysOfWeekType.values(), default=DaysOfWeekType.monday.value)
    today: date = ndb.DateProperty()
    time_on_duty: datetime = ndb.DateTimeProperty()
    time_of_duty: datetime = ndb.DateTimeProperty()    
    hourly_rate: int = ndb.IntegerProperty(default=config_instance.HOURLY_RATE)
    time_sheet_paid: bool = ndb.BooleanProperty(default=False)

    #   TODO add overtime rates

    @property
    def time_worked_hours(self) -> int:
        """
        **time_worked_hours**
            calculates the total time worked in hours
        :return: int -> total time worked in hours
        """
        if self.time_of_duty and self.time_on_duty:
            return (self.time_of_duty - self.time_on_duty).seconds // 3600
        return 0

    @property
    def time_worked_minutes(self) -> int:
        """
        **time_worked_minutes**
            calculates the total time worked in minutes
        :return: int -> total time worked in minutes
        """
        if self.time_of_duty and self.time_on_duty:
            return (self.time_of_duty - self.time_on_duty).seconds // 60
        return 0

    @property
    def calculate_pay(self) -> AmountMixin:
        """
        **calculate_pay**
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