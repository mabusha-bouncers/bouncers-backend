"""
    Bookings Module
        allows clients to place a booking for bouncers
        to attend their events
"""
from google.cloud import ndb
from src.models.basemodel import BaseModel


class BookingsModule(BaseModel):
    """

    """
    booking_id: str = ndb.StringProperty(indexed=True)