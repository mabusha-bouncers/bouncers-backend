"""
    Module serves to create a payment object
    in order to track client payments
"""
from google.cloud import ndb
from src.models.mixins import AmountMixin
from src.models.basemodel import BaseModel


class PaymentsModel(BaseModel):
    """a model to track client payments"""

    uid: str = ndb.StringProperty()
    amount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    date_paid: date = ndb.DateProperty(auto_now_add=True)
    time_paid: time = ndb.TimeProperty(auto_now_add=True)

    
    def __init__(self) -> None:
        super(PaymentsModel, self).__init__
    

    def __str__(self) -> str:
        return f""