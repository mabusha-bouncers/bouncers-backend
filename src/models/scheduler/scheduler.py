"""
    scheduler for:
        creating bouncers work schedule based on availability pf
        bouncer and also availability of work .

"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from datetime import datetime, date
from enum import Enum
from typing import List
from google.cloud import ndb
from src.models.basemodel import BaseModel


class DailySlotsTypes(Enum):
    """
    **Class DailySlotsTypes**
        there are three divisions of 8 hours each in a single day for which a user
    """
    morning = 'morning'
    evening = 'evening'
    late = 'late'

    @classmethod
    def types(cls):
        return list(cls)

    @classmethod
    def values(cls) -> List[str]:
        return [_slot.value for _slot in cls.types()]


class SchedulerModel(BaseModel):
    """
        **Class SchedulerModel**
            this class allows the application to keep track of work schedule
            depending on availability of Bouncers & Security Guards in Specific
            Areas, once Guards and Bouncers are available then Clients can Book them

        `PARAMETERS`
            schedule_id: str -> Indicates the time the schedule started running Note Schedules are ran for 8 hours at a time
            schedule_day: date ->
            time_slot: str ->
            location_address_id: str -> unique id for the address field
    """
    schedule_id: str = ndb.StringProperty(required=True)
    scheduled_day: date = ndb.DateProperty(auto_now_add=True)
    time_slot: str = ndb.StringProperty(choices=DailySlotsTypes.values())
    location_address_id: str = ndb.StringProperty(indexed=True, required=True)
    time_created: datetime = ndb.DateTimeProperty(auto_now_add=True)
    time_updated: datetime = ndb.DateTimeProperty(auto_now=True)

    def __str__(self) -> str:
        """ Returns the string representation of the object """
        return f"{self.schedule_id} - {self.time_slot} - {self.location_address_id}"

    def __eq__(self, other) -> bool:
        """ Returns True if the objects are equal """
        return self.schedule_id == other.schedule_id and self.time_slot == other.time_slot and self.location_address_id == other.location_address_id

    def __bool__(self) -> bool:
        """ Returns True if the object is not None """
        return bool(self.schedule_id) and bool(self.time_slot) and bool(self.location_address_id)


class BouncerScheduled(BaseModel):
    """
        **Class BouncerScheduled**
            this schedules a bouncer to a specific schedule

        `PARAMETERS`
            scheduled_id: str ->
            uid: str ->
    """
    schedule_id: str = ndb.StringProperty(required=True)
    uid: str = ndb.StringProperty(required=True)
    schedule_name: str = ndb.StringProperty(required=True)
    is_active: bool = ndb.BooleanProperty(default=True)
    time_created: datetime = ndb.DateTimeProperty(auto_now_add=True)
    time_updated: datetime = ndb.DateTimeProperty(auto_now=True)

    def __str__(self) -> str:
        return f"{self.schedule_name} - {self.is_active} - {self.time_created}"

    def __bool__(self) -> bool:
        return self.is_active and bool(self.uid) and bool(self.schedule_id)

    def __eq__(self, other) -> bool:
        return self.uid == other.uid and self.schedule_id == other.schedule_id
