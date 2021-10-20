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
            today datetime -> Indicates the time the schedule started running
                                        # Note Schedules are ran for 8 hours at a time
    """
    schedule_id: str = ndb.StringProperty(required=True)
    scheduled_day: date = ndb.DateProperty(auto_now_add=True)
    time_slot: str = ndb.StringProperty(choices=DailySlotsTypes.values())
    location_address_id: str = ndb.StringProperty(indexed=True, required=True)


class BouncerScheduled(BaseModel):
    """this schedules a bouncer to a specific schedule"""
    schedule_id: str = ndb.StringProperty(required=True)
    uid: str = ndb.StringProperty(required=True)

