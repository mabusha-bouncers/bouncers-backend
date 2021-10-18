"""
    Help desk model will take care of the following functionality:
        allows clients, and bouncers to send tickets/ reports
        detailing how they wish to be helped on the following topics,

            1. Payments
            2. Installing Web Applications / Android Application
            3. Resolving Technical Issues (Errors using the application(s) )
            4. How To (Several ways in which one can enable certain functionality on the applications)
            5. Notifications (setting up & Receiving )
"""
from datetime import date

from google.cloud import ndb
from src.models.basemodel import BaseModel


class HelpDesk(BaseModel):
    """
        **Class Helpdesk**

        **Parameters**

            uid: unique id for users
            ticket_id: unique id for this ticket
    """
    _min_length: int = 36
    uid: str = ndb.StringProperty(indexed=True)
    ticket_id: str = ndb.StringProperty(indexed=True)
    subject: str = ndb.StringProperty()
    body: str = ndb.StringProperty()
    ticket_type: str = ndb.StringProperty()
    is_resolved: str = ndb.BooleanProperty(default=False)
    date_created: date = ndb.DateProperty(auto_now_add=True)
    date_updated: date = ndb.DateProperty(auto_now=True)

    def __bool__(self) -> bool:
        return bool(self.uid)

    def __str__(self) -> str:
        """Allows printing of helpdesk"""
        return f"<Ticket: type: {self.ticket_type},  subject: {self.subject},  body: {self.body[0:self._min_length]}"
