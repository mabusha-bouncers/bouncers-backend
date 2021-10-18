"""
    scheduler for:
        creating bouncers work schedule based on availability pf
        bouncer and also availability of work .

"""
from google.cloud import ndb

from src.models.basemodel import BaseModel


class ScheduleModel(BaseModel):
    """
        **Class ScheduleModel**
    """
    schedule_id: str = ndb.StringProperty(required=True)
