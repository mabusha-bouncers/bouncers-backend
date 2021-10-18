"""
    module inherits from user and add bouncer specific functionality
"""
from google.cloud import ndb

from src.models.users import UserModel



class BouncerModel(UserModel):
    """
        **BouncerModel**
            adds bouncer specific functionality to userModel

        **PARAMETERS**
            available: True if bouncer is available to go on duty
            contact_preference: cell / email -> defaults to cell phone
    """
    available: bool = ndb.BooleanProperty(default=False)
    contact_preference: str = ndb.StringProperty(default='cell')
    location_address = ndb.StructuredProperty()