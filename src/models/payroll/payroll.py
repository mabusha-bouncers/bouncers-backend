"""
    A module to process payrolls

"""

class BankDetails(BaseModel):
    """
        A class to store bank details
    """
    uid: str = ndb.StringProperty(indexed=True, required=True)
    account_name = ndb.StringProperty(required=True)
    account_type = ndb.StringProperty(required=True)
    bank_name = ndb.StringProperty(required=True)
    account_number = ndb.StringProperty(required=True)
    branch_code = ndb.StringProperty(required=True)
    

class PayrollProcessing(BaseModel):
    """
        A class to process payrolls
    """
    uid: str = ndb.StringProperty(required=True)
    amount_to_pay: AmountMixin = ndb.StructuredProperty(AmountMixin, required=True)
    is_paid: bool = ndb.BooleanProperty(required=True)
    date_paid: datetime.date = ndb.DateProperty(required=True)
    date_created: datetime.date = ndb.DateProperty(required=True)
    date_updated: datetime.date = ndb.DateProperty(required=True)


    @property
    def bank_details(self) -> dict:
        """
        ** Get bank details **
            A method to get bank details
        """
        bank_details = BankDetails.query(BankDetails.uid == self.uid).fetch()
        return bank_details.to_dict()

    def send_payment_notification(self):
        """
        ** Send a notification to bouncer **
            A method to send payment notification
        """
        pass
