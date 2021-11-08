"""
    **Payslips**
        this is a model for payslips database table

        1. Vehicle and Shooter War Rooms
        2. Garrison Hall Building
        3. Anti Missilie Defense Center
        4. Silo 
        5. Blast Missile Factory
        if any of this buildings is still at a low level choose the one you want to do and get it up to level 10 2 will be better

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
    bonus: int = ndb.IntegerProperty(indexed=True, required=True)
    total: int = ndb.IntegerProperty(indexed=True, required=True)
    is_bonus_paid: bool = ndb.BooleanProperty(indexed=True, required=True)
    is_paid_to_bouncer: bool = ndb.BooleanProperty(indexed=True, required=True)
    

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
        

    def pay_bouncer(self) -> bool:
        """
            **pay_bouncer**
                pays bouncer
        """
        from src.models.users.bouncer import BouncerModel
        bouncer_instance = BouncerModel.query(BouncerModel.uid == self.uid).get()
        if isinstance(bouncer_instance, BouncerModel) and bool(bouncer_instance):
            bouncer_instance.pay_salary(self.total)
            self.is_paid_to_bouncer = True
            self.put()
            return True
        return False

    def pay_bonus_to_bouncer(self) -> bool:
        """
            **pay_bonus_to_bouncer**
                pays bouncer bonus
        """
        from src.models.users.bouncer import BouncerModel
        bouncer_instance = BouncerModel.query(BouncerModel.uid == self.uid).get()
        if isinstance(bouncer_instance, BouncerModel) and bool(bouncer_instance):
            bouncer_instance.pay_bonus(self.bonus)
            self.is_bonus_paid = True
            self.put()
            return True
        return False



    