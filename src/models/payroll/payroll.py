"""
    A module to process payrolls

"""
from datetime import datetime

from google.cloud import ndb
from src.models.basemodel import BaseModel
from src.models.mixins import AmountMixin


class BankDetails(BaseModel):
    """
        **BankDetails**
            A class to store bank details, for the processing of payrolls
    """
    uid: str = ndb.StringProperty(indexed=True, required=True)
    account_name = ndb.StringProperty(required=True)
    account_type = ndb.StringProperty(required=True)
    bank_name = ndb.StringProperty(required=True)
    account_number = ndb.StringProperty(required=True)
    branch_code = ndb.StringProperty(required=True)

    def __str__(self) -> str:
        return f"{self.account_name} - {self.bank_name} - {self.account_number}"

    def __bool__(self) -> bool:
        return bool(self.account_name) and bool(self.bank_name) and bool(self.account_number) and bool(self.uid)

    def __eq__(self, other: 'BankDetails') -> bool:
        return self.uid == other.uid


class PayrollProcessingModel(BaseModel):
    """
        A class to process payrolls
    """
    uid: str = ndb.StringProperty(required=True)
    amount_to_pay: AmountMixin = ndb.StructuredProperty(AmountMixin, required=True)
    is_paid: bool = ndb.BooleanProperty(default=False, required=True)
    date_paid: datetime.date = ndb.DateProperty(required=True)
    date_created: datetime.date = ndb.DateProperty(auto_now_add=True)
    date_updated: datetime.date = ndb.DateProperty(auto_now=True)

    @property
    def bank_details(self) -> dict:
        """
        ** Get bank details **
            A method to get bank details
        """
        bank_details = BankDetails.query(BankDetails.uid == self.uid).fetch()
        return bank_details.to_dict()

    def add_bank_details(self, bank_details: dict):
        """
        ** Add bank details **
            A method to add bank details
        """
        bank_details = BankDetails.query(BankDetails.uid == self.uid).fetch()
        if isinstance(bank_details, BankDetails) and bool(bank_details):
            return bank_details
        else:
            bank_details = BankDetails(uid=self.uid, **bank_details)
            bank_details.put()
            return bank_details

    def send_payment_notification(self):
        """
        ** Send a notification to bouncer **
            A method to send payment notification
        """
        pass

    def make_payment(self):
        """
        ** Make a payment **
            A method to be called after payment is actually sent to bouncers bank account
        """
        pass

    def __str__(self) -> str:
        return f"{self.amount_to_pay} - {self.is_paid} - {self.date_paid} - {self.date_created} - {self.date_updated}"

    def __eq__(self, other: 'PayrollProcessing') -> bool:
        return self.uid == other.uid
