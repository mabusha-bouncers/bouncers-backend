"""
    Bookings Module
        allows clients to place a booking for bouncers
        to attend their events
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from google.cloud import ndb
from src.models.basemodel import BaseModel


class BookingsModule(BaseModel):
    """

    """
    booking_id: str = ndb.StringProperty(indexed=True)