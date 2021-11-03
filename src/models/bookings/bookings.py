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


class BookingsModel(BaseModel):
    """
        **BookingsModel**
            allows clients to book bouncers
    """
    booking_id: str = ndb.StringProperty(indexed=True)
    client_id: str = ndb.StringProperty(indexed=True)

    date_booked: date = ndb.DateProperty(auto_now_add=True)
    time_booked: time = ndb.TimeProperty(auto_now_add=True)
    



