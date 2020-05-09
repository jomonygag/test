from django.contrib import admin

# Register your models here.

from .models import TransactionData


class TransactionDataAdmin(admin.ModelAdmin):
    model = TransactionData

    list_display = (
        'order_reference', 'amount', 'currency', 'customer_name', 'customer_email', 'idempotency_key',
        'payment_reference',
        'status')


admin.site.register(TransactionData, TransactionDataAdmin)
