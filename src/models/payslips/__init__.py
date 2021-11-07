"""
    **Payslips**
        this is a model for payslips database table

"""
from src.models.basemodel import BaseModel
from google.cloud import ndb



class PaySlip(BaseModel):
    """
        **PaySlip**
            a model for payslips database table
    """
    uid: str = ndb.StringProperty(indexed=True, required=True)
    employee_id: str = ndb.StringProperty(indexed=True, required=True)
    pay_date: date = ndb.DateProperty(indexed=True, required=True)
    hours: int = ndb.IntegerProperty(indexed=True, required=True)
    rate: int = ndb.IntegerProperty(indexed=True, required=True)
    amount: int = ndb.IntegerProperty(indexed=True, required=True)

    @property
    def bouncer_details(self) -> Optional[dict]:
        """
            **bouncer_details**
                returns bouncer details - names, surname, cell, email & address
        """
        from src.models.users.bouncer import BouncerModel
        bouncer_instance = BouncerModel.query(BouncerModel.uid == self.uid).get()
        if isinstance(bouncer_instance, BouncerModel) and bool(bouncer_instance):
            return bouncer_instance.to_dict()
        return None

    