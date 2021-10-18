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
    """
    uid: str = ndb.StringProperty(indexed=True)
    today: date = ndb.DateProperty()
    time_on_duty: datetime = ndb.DateTimeProperty()
    time_of_duty: datetime = ndb.DateTimeProperty()
    time_worked_minutes: int = ndb.IntegerProperty()
