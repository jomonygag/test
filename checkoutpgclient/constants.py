from django.utils.translation import ugettext as _

PAYMENT_STATUS_AUTHORIZED = 'Authorized'
PAYMENT_STATUS_CAPUTRED = 'Captured'
PAYMENT_STATUS_CARD_VERIFIED = 'Card Verified'
PAYMENT_STATUS_DECLINED = 'Declined'
PAYMENT_STATUS_PENDING = 'Pending'
PAYMENT_STATUS_VOIDED = 'Voided'
PAYMENT_STATUS_PARTIALLY_CAPTURED = 'Partially Captured'
PAYMENT_STATUS_PARTIALLY_REFUNDED = 'Partially Refunded'
PAYMENT_STATUS_REFUNDED = 'Refunded'
PAYMENT_STATUS_CANCELLED = 'Cancelled'
PAYMENT_STATUS_PAID = 'Paid'
PAYMENT_STATUS_NONE = 'None'

PAYMENT_STATUS_CHOICES = (
    (PAYMENT_STATUS_NONE, _('None')),
    (PAYMENT_STATUS_AUTHORIZED, _('Authorized')),
    (PAYMENT_STATUS_CAPUTRED, _('Captured')),
    (PAYMENT_STATUS_CARD_VERIFIED, _('Card Verified')),
    (PAYMENT_STATUS_DECLINED, _('Declined')),
    (PAYMENT_STATUS_PENDING, _('Pending')),
    (PAYMENT_STATUS_VOIDED, _('Voided')),
    (PAYMENT_STATUS_PARTIALLY_CAPTURED, _('Partially Captured')),
    (PAYMENT_STATUS_PARTIALLY_REFUNDED, _('Partially Refunded')),
    (PAYMENT_STATUS_REFUNDED, _('Refunded')),
    (PAYMENT_STATUS_CANCELLED, _('Cancelled')),
    (PAYMENT_STATUS_PAID, _('Paid'))
)
