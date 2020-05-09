import json
import logging
from contextlib import contextmanager
from time import sleep

import redis
from checkoutpgclient.models import TransactionData
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from checkoutpgclient.libs.authentication import SignatureAuthentication

logger = logging.getLogger(__name__)


class WebhookListener(APIView):
    authentication_classes = (
            SignatureAuthentication,
        )

    def post(self, request):
        request_data = json.loads(str(request.data))

        try:
            invoice_pk = self.get_invoice_id(str(request_data.get('payment_reference', None)))

            lock_name = 'lock:WebhookListener:invoice_%d' % (int(invoice_pk),)
            with wait_lock(lock_name=lock_name):

                transaction, created = TransactionData.objects.select_for_update().get_or_create(
                    invoice_id=str(invoice_pk),
                    defaults={'order_reference': str(request_data.get('idempotency_key', None)),
                              'amount': str(request_data.get('amount', None)),
                              'currency': str(request_data.get('currency', None)),
                              'customer_name': str(request_data.get('customer_name', None)),
                              'customer_email': str(request_data.get('customer_email', None)),
                              'payment_reference': str(request_data.get('payment_reference', None)),
                              'request_source': str(request_data.get('request_source', None)),
                              'api_request_data': str(request_data.get('api_request_data', None)),
                              'api_response_data': str(request_data.get('api_response_data', None)),
                              'is_notification': request_data.get('is_notification', None),
                              'approved': request_data.get('approved', None),
                              'status': str(request_data.get('status', None)),
                              'auth_code': str(request_data.get('auth_code', None)),
                              'response_summary': str(request_data.get('response_summary', None)),

                              'idempotency_key': str(request_data.get('idempotency_key'))}
                )
                if not created:
                    transaction.approved = request_data.get('approved')
                    transaction.status = str(request_data.get('status'))
                    transaction.auth_code = request_data.get('auth_code')
                    transaction.response_summary = str(request_data.get('response_summary'))
                    transaction.api_response_data = str(request_data.get('api_response_data'))
                    transaction.payment_reference = str(request_data.get('payment_reference'))

                    transaction.save()
                response_data = {'message': "Checkout webhook listener successfully processed data"}
                return self.pg_response('HTTP_200_OK', data=response_data)
        except:
            response_data = {'message': "Data not  updated"}
            return self.pg_response('HTTP_500_INTERNAL_SERVER_ERROR', data=response_data)

    def get_invoice_id(self, paymentrefernce):
        paymentrefernce = paymentrefernce.split('-')
        invoice_id = paymentrefernce[2].split('|')
        invoice_id = invoice_id[0]
        return invoice_id

    def pg_response(self, code='HTTP_200_OK', data=None):
        return Response(
            headers={'status': getattr(status, code)},
            status=getattr(status, code),
            data={
                'status': getattr(status, code),
                'data': data
            },
            content_type='application/json'
        )


@contextmanager
def wait_lock(
        lock_name, lock_timeout=settings.WAIT_LOCK_DEFAULT_TIMEOUT,
        wait_duration=settings.WAIT_LOCK_DEFAULT_WAIT_DURATION,
        max_retries=settings.WAIT_LOCK_DEFAULT_MAX_RETRIES):
    """
    Executes code if lock `lock_name` isn't set, else it retries after
    `wait_duration` seconds.

    Context manager for making sure only one single process/thread
    executes a piece of code with a given `lock_name`.  If the lock for
    the process is already set then it waits for `wait_duration` seconds
    up to `max_retries` times.  To prevent the lock from being set for a
    long time, in case of errors, it will expire after `lock_timeout`
    seconds.

    """
    redis_conn = redis.StrictRedis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT,
        db=settings.REDIS_LOCKS_DB
    )

    retries = 0
    while redis_conn.get(lock_name):
        if retries < max_retries:
            logger.debug("Lock exists...sleeping.")
            sleep(wait_duration)
            retries += 1
        else:
            raise Exception('Unable to acquire lock.')

    redis_conn.setex(lock_name, lock_timeout, '1')
    try:
        yield
    finally:
        redis_conn.delete(lock_name)
