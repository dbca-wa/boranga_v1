[![Build
status](https://travis-ci.org/dbca-wa/boranga.svg?branch=master)](https://travis-ci.org/dbca-wa/boranga/builds) [![Coverage Status](https://coveralls.io/repos/github/dbca-wa/boranga/badge.svg?branch=master)](https://coveralls.io/github/dbca-wa/boranga?branch=master)
# Commercial Operator Licensing System

The Commercial Operator Licensing System (COLS) is used by customers applying for a licence to deliver tourist and educational services for a profit while on land managed by the Department and to pay for the access fees to access these lands. The system is used by Department staff to process the licence applications and to manage issued licences.

It is a database-backed Django application, using REST API with Vue.js as the client side app and integrates into the ledger system.

# Requirements

- Python (2.7.x)
- PostgreSQL (>=9.3)

Python library requirements should be installed using `pip`:

`pip install -U setuptools==44.0.0`
`pip install -r requirements.txt`

# Environment settings

A `.env` file should be created in the project root and used to set
required environment variables at run time. Example content:

    DEBUG=True
    SECRET_KEY='thisismysecret'
    DATABASE_URL='postgis://user:pw@localhost:port/db_name'
    EMAIL_HOST='SMTP_HOST'
    BPOINT_USERNAME='BPOINT_USER'
    BPOINT_PASSWORD='BPOINT_PW
    BPOINT_BILLER_CODE='1234567'
    BPOINT_MERCHANT_NUM='BPOINT_MERCHANT_NUM'
    BPAY_BILLER_CODE='987654'
    CMS_URL="CMS_URL"
    LEDGER_USER="LEDGER_USER"
    LEDGER_PASS="LEDGER_PASS"
    OSCAR_SHOP_NAME='SHOP_NAME'
    DEFAULT_COLS_EMAIL='DEFAULT_EMAIL_ADDRESS'
    DEFAULT_FROM_EMAIL='FROM_EMAIL_ADDRESS'
    NOTIFICATION_EMAIL='NOTIF_RECIPIENT_1, NOTIF_RECIPIENT_2'
    NON_PROD_EMAIL='NON_PROD_RECIPIENT_1, NON_PROD_RECIPIENT_2'
    EMAIL_INSTANCE='DEV'
    PRODUCTION_EMAIL=False
    BPAY_ALLOWED=False
    SITE_PREFIX='cols-dev'
    SITE_DOMAIN='SITE_DOMAIN'
    LEDGER_GST=10
    DISABLE_EMAIL=True
    PS_PAYMENT_SYSTEM_ID='S123'

