import json
from rest_framework import viewsets, status
from rest_framework.response import Response

from checkoutpgclient.models import TransactionData
from checkoutpgclient.v1.serializers.transaction_serializer import TransactionDataSerializer


class PaymentInterface:

    def get_payment_status(self, reference_number):

        payment_object = self.get_paymentobject(reference_number)
        if payment_object:
            return payment_object.status
        return None

    def get_payment_rawdata(self, reference_number):
        payment_object = self.get_paymentobject(reference_number)
        if payment_object:
            serializer = TransactionDataSerializer(payment_object)
            return serializer.data
        return None

    def get_paymentobject(self, reference_number):
        try:
            payment_object = TransactionData.objects.filter(payment_reference=str(reference_number)).last()
        except Exception as e:
            return None
        return payment_object
