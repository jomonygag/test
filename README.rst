=====
Payment
=====

Payment is a Django app to conduct handle checkoutPg responses.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1.Install the package
    ``pip install django-CheckoutpgClient-Py2-Django1-0.1.tar.gz``

2. Add "payment" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'checkoutpgclient',
    ]

3. Include the polls URLconf in your project urls.py like this::

    path('checkoutpg/', include('checkoutpgclient.urls')),

4. Add your api and secret keys to settings.py

    ``CHEKOUTPG_API_KEY = '< your api-key >'``
    ``CHEKOUTPG_SECRET_KEY = '< your secret-key >'``


5. Run ``python manage.py migrate`` to create the polls models.

6. Visit ``http://127.0.0.1:8000/checkoutpg-client-hook/`` to this url checkoutpg will push data