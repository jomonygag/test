
from django.db import models
from django.utils.translation import ugettext as _
from .constants import (PAYMENT_STATUS_CHOICES, PAYMENT_STATUS_NONE)


class TransactionData(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    order_reference = models.CharField(max_length=200)
    amount = models.DecimalField(decimal_places=4, max_digits=12)
    currency = models.CharField(max_length=3)
    customer_name = models.CharField(max_length=200)
    customer_email = models.CharField(max_length=500)
    idempotency_key = models.CharField(
        max_length=200, blank=False, default=None,
        help_text=_('Unique key to avoid duplicate payment happening due to '
                    'network error or timeout. Recommend to use V4 UUIDs.'))
    payment_reference = models.CharField(
        max_length=200, blank=False, help_text=_('Payment reference number'))
    request_source = models.CharField(
        max_length=100, null=True, blank=True,
        help_text=_('Represent source from where this payment request '
                    'initiated'))
    api_request_data = models.TextField(
        null=True, blank=True, help_text=_('Payment API request data'))
    api_response_data = models.TextField(
        null=True, blank=True, help_text=_('Payment API response data'))
    is_notification = models.BooleanField(default=False)
    approved = models.BooleanField(
        default=False,
        help_text=_('Denotes whether payment is approved or not'))
    status = models.CharField(max_length=200, choices=PAYMENT_STATUS_CHOICES,
                              default=PAYMENT_STATUS_NONE,
                              help_text=_('Payment status'))
    auth_code = models.CharField(
        max_length=50, null=True, blank=True,
        help_text=_('The acquirer authorization code, if the payment '
                    'was authorized.'))
    response_summary = models.CharField(
        max_length=500, null=True, blank=True,
        help_text=_('Checkout response summary text'))
    invoice_id = models.CharField(
        max_length=50, null=True, blank=True,
        help_text=_('invoice pk that response associated with'))


