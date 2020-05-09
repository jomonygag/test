
from django.conf.urls import patterns
from django.conf.urls import url
from checkoutpgclient import signals

from checkoutpgclient.v1.views.webhook_listener import WebhookListener

urlpatterns = patterns('',
                       url(r'^webhook/$', WebhookListener.as_view(), name='payment'),
                       )
