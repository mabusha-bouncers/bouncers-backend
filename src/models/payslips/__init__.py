"""
    **Payslips**
        this is a model for payslips database table

"""
from src.models.basemodel import BaseModel
from src.models.mixins import AmountMixin
from google.cloud import ndb



class PaySlip(BaseModel):
    """
        **PaySlip**
            a model for payslips database table
    """
    uid: str = ndb.StringProperty(indexed=True, required=True)
    employee_id: str = ndb.StringProperty(indexed=True, required=True)
    pay_date: date = ndb.DateProperty(indexed=True, required=True)
    minutes: int = ndb.IntegerProperty(indexed=True, required=True)
    rate: float = ndb.FloatProperty(indexed=True, required=True)
    bonus: AmountMixin = ndb.StructuredProperty(AmountMixin, required=True)
    is_bonus_paid: bool = ndb.BooleanProperty(indexed=True, required=True)
    is_paid_to_bouncer: bool = ndb.BooleanProperty(indexed=True, required=True)
    


    @property
    def hours(self) -> float:
        """
            **hours**
                returns hours
        """
        return self.minutes / 60

    @property
    def normal_pay(self) -> AmountMixin:
        """
            **normal pay amount**
                returns amount to pay to bouncers based on rate and hours worked
        """
        # TODO have to make rate dependent on bouncer rating
        return AmountMixin(amount_in_cents=int(self.hours * self.rate * 100), currency=config_instance.currency)

    @property
    def total_amount(self) -> AmountMixin:
        """
            **total_amount**
                returns total amount to pay to bouncers  based on rate and hours worked + bonus 
                if bonus is to be paid separately then use total and bonus figures separately
        """
        return AmountMixin(amount_in_cents=self.normal_pay.amount_in_cents + self.bonus.amount_in_cents, currency=config_instance.currency)

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
        

    def pay_normal_pay_to_bouncer(self) -> bool:
        """
            **pay_bouncer**
                pays bouncer normal pay
        """
        from src.models.users.bouncer import BouncerModel
        bouncer_instance = BouncerModel.query(BouncerModel.uid == self.uid).get()
        if isinstance(bouncer_instance, BouncerModel) and bool(bouncer_instance):
            bouncer_instance.pay_salary(self.normal_pay)
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



    def pay_total_amount_to_bouncer(self) -> bool:
        """
            **pay_total_amount_to_bouncer**
                pays bouncer total amount   
        """
        from src.models.users.bouncer import BouncerModel
        bouncer_instance = BouncerModel.query(BouncerModel.uid == self.uid).get()
        if isinstance(bouncer_instance, BouncerModel) and bool(bouncer_instance):
            bouncer_instance.pay_salary(self.normal_pay)
            bouncer_instance.pay_bonus(self.bonus)
            self.is_paid_to_bouncer = True
            self.put()
            return True
        return False