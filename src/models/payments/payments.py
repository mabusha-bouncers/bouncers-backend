"""
    Module serves to create a payment object
    in order to track client payments
"""
from datetime import date, datetime
from typing import List
from google.cloud import ndb
from src.models.mixins import AmountMixin
from src.models.basemodel import BaseModel
from enum import Enum, auto


class PaymentTypes(Enum):
    """
        Enum for payment types
    """
    cash = auto()
    credit = auto()
    debit = auto()

    @classmethod
    def choices(cls) -> List[str]:
        """
            Method to return a list of payment choices
        """
        return [choice.name for choice in cls]


class PaymentsModel(BaseModel):
    """
    **Class PaymentsModel**
        a model to track client payments

    `Properties`
        - **payment_id**: payment id
        - **uid**: user id
        - **amount**: amount paid
        - **date**: date of payment
        - **payment_type**: payment type
    """

    uid: str = ndb.StringProperty()
    payment_id: str = ndb.StringProperty()
    amount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    payment_type: str = ndb.StringProperty(choices=PaymentTypes.choices())
    date_created: date = ndb.DateProperty(auto_now_add=True)
    payment_approved: bool = ndb.ComputedProperty(lambda self: self.time_approved is not None)
    time_approved: datetime = ndb.DateTimeProperty()
    is_paid: bool = ndb.ComputedProperty(lambda self: self.time_paid is not None)
    time_paid: datetime = ndb.DateTimeProperty()

    def __str__(self) -> str:
        """
            Method to return a string representation of the object
        """
        return f"{self.payment_id} - {self.amount} - {self.payment_type}"

    def __bool__(self) -> bool:
        """
            Method to return a boolean representation of the object
        """
        return bool(self.payment_id)

    def __eq__(self, other) -> bool:
        """
            Method to compare two objects
        """
        return self.payment_id == other.payment_id

    def approve(self) -> bool:
        """
            Method to approve a payment
        """
        self.time_approved = datetime.now()
        return self.put()

    def reject(self) -> bool:
        """
            Method to reject a payment
        """
        self.time_approved = None
        return self.put()

    def paid(self) -> bool:
        """
            Method to mark a payment as paid
        """
        self.time_paid = datetime.now()
        return self.put()
