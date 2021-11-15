"""
    Payments View Model
        allows clients to create, view and update payments

"""
from flask import jsonify
from google.cloud import ndb
from src.models.payments import PaymentsModel
from src.exceptions.exceptions import DataServiceError, InputError, status_codes
from src.utils.utils import create_id, date_string_to_date
from src.views import ViewModel


class PaymentView(ViewModel):
    """ 
    **Class PaymentView**
        Payment View Model , allows for the creation, viewing and updating of payments
    
    """
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def __init__(self):
        super().__init__()

    @staticmethod
    def get(payment_id: str) -> tuple:
        """ get a payment """
        if payment_id is None:
            raise InputError(description='Payment ID is required')

        payment_instance: PaymentsModel = PaymentsModel.query(PaymentsModel.payment_id == payment_id).get()

        if not isinstance(payment_instance, PaymentsModel):
            return jsonify(dict(status=False,
                                message='payment with that payment id is not found')), status_codes.data_not_found_code

        return jsonify(dict(status=True,
                            payload=payment_instance.to_dict(),
                            message='successfully retrieved payment')), status_codes.status_ok_code

    @staticmethod
    def post(payment_data: dict) -> tuple:
        """
        **post**
        create a payment """
        if payment_data is None:
            raise InputError(description='Payment data is required')

        payment_instance: PaymentsModel = PaymentsModel(**payment_data, payment_id=create_id())

        key: ndb.Key = payment_instance.put()
        if not isinstance(key, ndb.Key):
            raise DataServiceError(description='Failed to create payment')

        return jsonify(dict(status=True,
                            payload=payment_instance.to_dict(),
                            message='successfully created payment')), status_codes.status_ok_code

    @staticmethod
    def put(payment_data: dict) -> tuple:
        """ update a payment """
        if payment_data is None:
            raise InputError(description='Payment data is required')

        payment_instance: PaymentsModel = PaymentsModel.query(
            PaymentsModel.payment_id == payment_data['payment_id']).get()
        if not isinstance(payment_instance, PaymentsModel):
            return jsonify(dict(status=False,
                                message='payment with that payment id is not found')), status_codes.data_not_found_code

        payment_instance.update(**payment_data)
        key: ndb.Key = payment_instance.put()
        if not isinstance(key, ndb.Key):
            raise DataServiceError(description='Failed to update payment')

        return jsonify(dict(status=True,
                            payload=payment_instance.to_dict(),
                            message='successfully updated payment')), status_codes.successfully_updated_code

    @staticmethod
    def delete(payment_id: str) -> tuple:
        """ delete a payment """
        if payment_id is None:
            raise InputError(description='Payment ID is required')

        payment_instance: PaymentsModel = PaymentsModel.query(PaymentsModel.payment_id == payment_id).get()
        if not isinstance(payment_instance, PaymentsModel):
            return jsonify(dict(status=False,
                                message='payment with that payment id is not found')), status_codes.data_not_found_code

        payment_instance.key.delete()
        return jsonify(dict(status=True,
                            message='successfully deleted payment')), status_codes.status_ok_code


class PaymentListView(ViewModel):
    """
        **Class PaymentListView**
            enables access to a list of payment records
    """
    methods = ['GET']

    def __init__(self):
        """initialize the payment list view"""
        super().__init__()

    @staticmethod
    def get() -> tuple:
        """ 
        **return a list of payments**
            returns a complete list of all payments every made by the system
        """
        payment_list: list = PaymentsModel.query().fetch()
        if not isinstance(payment_list, list):
            return jsonify(dict(status=False,
                                message='failed to retrieve payment list')), status_codes.data_not_found_code

        return jsonify(dict(status=True,
                            payload=[payment.to_dict() for payment in payment_list],
                            message='successfully retrieved payment list')), status_codes.status_ok_code


class PaymentListByClientView(ViewModel):
    """
        **Class PaymentListByClientView**
            will return a list of payments made by a client
            
    """
    methods = ['GET']

    def __init__(self):
        """initialize the payment list view"""
        super().__init__()

    @staticmethod
    def get(client_id: str) -> tuple:
        """ 
        **return a list of payments**
            returns a complete list of all payments made by a client
        """
        if client_id is None:
            raise InputError(description='Client ID is required')

        payment_list: list = PaymentsModel.query(PaymentsModel.client_id == client_id).fetch()
        if not isinstance(payment_list, list):
            return jsonify(dict(status=False,
                                message='failed to retrieve payment list')), status_codes.data_not_found_code

        return jsonify(dict(status=True,
                            payload=[payment.to_dict() for payment in payment_list],
                            message='successfully retrieved payment list')), status_codes.status_ok_code


class PaymentListByClientAndDateView(ViewModel):
    """
        **Class PaymentListByClientAndDateView**
            will return a list of payments made by a client in a specific date
        

    """
    methods = ['GET']

    def __init__(self):
        """initialize the payment list view"""
        super().__init__()

    @staticmethod
    def get(client_id: str, date_created: str) -> tuple:
        """ 
        **return a list of payments**
            returns a list of payments made by a client in a specific date
        """
        if client_id is None:
            raise InputError(description='Client ID is required')

        if date_created is None:
            raise InputError(description='Date is required')
        _date_created = date_string_to_date(date_created)
        payment_list: list = PaymentsModel.query(PaymentsModel.client_id == client_id,
                                                 PaymentsModel.date_created == _date_created).fetch()
        if not isinstance(payment_list, list):
            return jsonify(dict(status=False,
                                message='failed to retrieve payment list')), status_codes.data_not_found_code

        return jsonify(dict(status=True,
                            payload=[payment.to_dict() for payment in payment_list],
                            message='successfully retrieved payment list')), status_codes.status_ok_code
