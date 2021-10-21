"""
    Mixins for ndb.MODELS
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from datetime import date

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
    uid: str = ndb.StringProperty(required=True, indexed=True)
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
        return f"<User {self.email}"

    def __bool__(self) -> bool:
        return bool(self.email)


class FeedbackMixin(BaseModel):
    """
        **FeedbackMixin**
            mixin class for client and bouncer feedback models
        `PARAMETERS`
            client_uid: str = unique id for client
            bouncer_uid: str = unique id for bouncer
            feedback: str = feedback text if any
            date_updated: date = auto field
            date_created: date = auto field
    """
    client_uid: str = ndb.StringProperty()
    bouncer_uid: str = ndb.StringProperty()
    feedback: str = ndb.StringProperty()
    date_created: date = ndb.DateProperty(auto_now_add=True)
    date_updated: date = ndb.DateProperty(auto_now=True)

    def __bool__(self) -> bool:
        return bool(self.client_uid) and bool(self.bouncer_uid)
