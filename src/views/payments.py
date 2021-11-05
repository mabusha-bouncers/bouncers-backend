"""
    Payments View Model
        allows clients to create, view and update payments

"""
from flask import jsonify
from src.models.payments import PaymentsModel
from src.exceptions.exceptions import DataServiceError, InputError, status_codes

class PaymentView(ViewModel):
    """ Payment View Model """
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def get(self, payment_id: str) -> tuple:
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



