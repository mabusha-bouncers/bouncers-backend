"""
    Module serves to create a payment object
    in order to track client payments
"""
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
    payment_approved: bool = ndb.BooleanProperty(default=False)
    time_approved: datetime = ndb.DateTimeProperty()
    date_paid: date = ndb.DateProperty(auto_now_add=True)
    time_paid: time = ndb.TimeProperty(auto_now_add=True)

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
        self.payment_approved = True
        self.time_approved = datetime.now()
        return self.put()