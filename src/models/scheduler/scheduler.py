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

from google.cloud import ndb

from src.models.basemodel import BaseModel


class SchedulerModel(BaseModel):
    """
        **Class SchedulerModel**
    """
    schedule_id: str = ndb.StringProperty(required=True)
