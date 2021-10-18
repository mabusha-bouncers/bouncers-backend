"""
    Time Sheets module allows
        for keeping track of time worked by each bouncer
"""
from datetime import date, datetime
from google.cloud import ndb

from src.models.basemodel import BaseModel


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
    today: date = ndb.DateProperty()
    time_on_duty: datetime = ndb.DateTimeProperty()
    time_of_duty: datetime = ndb.DateTimeProperty()
    time_worked_hours: int = ndb.IntegerProperty()
    hourly_rate: int = ndb.IntegerProperty()
