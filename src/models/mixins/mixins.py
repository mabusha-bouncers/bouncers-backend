"""
    Mixins for ndb.MODELS
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from src.models.basemodel import BaseModel
from google.cloud import ndb
from src.config import config_instance
from src.models.property import property_


class AmountMixin(BaseModel):
    """
    **Class AmountMixin**
        A mixin to represent Money in cents

    **Class Properties**
        1. property: Amount: Integer -> Money in Cents
        2. property: Currency: String ->  Currency symbol
    """
    amount_cents: int = ndb.IntegerProperty(default=None, validator=property_.set_value_amount)
    currency: str = ndb.StringProperty(default=config_instance.CURRENCY, validator=property_.set_currency)

    @property
    def amount(self) -> int:
        return self.amount_cents

    @amount.setter
    def amount(self, value) -> None:
        self.amount_cents = value

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.amount_cents != other.amount_cents:
            return False
        if self.currency != other.currency:
            return False
        return True

    def __add__(self, other) -> any:
        # TODO - does not function properly it needs to return AmountMixin as results
        if self.__class__ != other.__class__:
            raise TypeError("Invalid type")
        if self.currency != other.currency:
            raise TypeError("Incompatible Currency")
        self.amount_cents += other.amount_cents
        return self

    def __sub__(self, other) -> any:
        # TODO - does not function properly it needs to return AmountMixin as results
        if self.__class__ != other.__class__:
            raise TypeError("Invalid type")
        if self.currency != other.currency:
            raise TypeError("Incompatible Currency")
        self.amount_cents -= other.amount_cents
        return self

    def __str__(self) -> str:
        return "Amount: {} {}".format(self.currency, self.amount_cents)

    def __bool__(self) -> bool:
        # if term payment amount is set to even zero bool will return True
        return bool(self.amount_cents) and bool(self.currency)


class UserMixin(BaseModel):
    """
        **Class UserMixin**
            handling user login properties of User Class -
            Passwords Hash are handled by werkzeug.security using the method : "pbkdf2:sha256"

        **Class Properties**
            1. Property: Email : String -> email password
            2. Property: Password : String -> User Password - will be converted to a password hash
    """
    email: str = ndb.StringProperty(validator=property_.set_email)
    password: str = ndb.StringProperty(validator=property_.set_password)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.email != other.email:
            return False
        if self.password != other.password:
            return False
        return True

    def __str__(self) -> str:
        return "<User {}".format(self.email)

    def __bool__(self) -> bool:
        return bool(self.email)
