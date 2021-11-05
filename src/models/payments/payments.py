"""
    Module serves to create a payment object
    in order to track client payments
"""
from google.cloud import ndb
from src.models.mixins import AmountMixin
from src.models.basemodel import BaseModel

class PaymentTypes(Enum):
    """
        Enum for payment types
    """
    CASH = 1
    CREDIT = 2
    DEBIT = 3
    

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
    date_paid: date = ndb.DateProperty(auto_now_add=True)
    time_paid: time = ndb.TimeProperty(auto_now_add=True)

    
    def __init__(self) -> None:
        super(PaymentsModel, self).__init__
    

    def __str__(self) -> str:
        return f""