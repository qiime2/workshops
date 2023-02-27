# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from .shared import (
    env,
    BASE_DIR,
    PROJ_DIR,
    INSTALLED_APPS,
    MIDDLEWARE,
    ROOT_URLCONF,
    TEMPLATES,
    WSGI_APPLICATION,
    DATABASES,
    AUTH_PASSWORD_VALIDATORS,
    LANGUAGE_CODE,
    TIME_ZONE,
    USE_I18N,
    USE_L10N,
    USE_TZ,
    STATIC_URL,
    STATICFILES_DIRS,
    STATIC_ROOT,
    APPEND_SLASH,
    DATA_UPLOAD_MAX_NUMBER_FIELDS,
)


__all__ = [
    'BASE_DIR',
    'PROJ_DIR',
    'SECRET_KEY',
    'DEBUG',
    'ALLOWED_HOSTS',
    'INSTALLED_APPS',
    'MIDDLEWARE',
    'ROOT_URLCONF',
    'TEMPLATES',
    'WSGI_APPLICATION',
    'DATABASES',
    'AUTH_PASSWORD_VALIDATORS',
    'LANGUAGE_CODE',
    'TIME_ZONE',
    'USE_I18N',
    'USE_L10N',
    'USE_TZ',
    'STATIC_URL',
    'STATICFILES_DIRS',
    'STATIC_ROOT',
    'APPEND_SLASH',
    'EMAIL_BACKEND',
    'DATA_UPLOAD_MAX_NUMBER_FIELDS',

    # BUSINESS LOGIC
    'ADMINS',
    'LMID',
    'PAYMENT_URL',
    'PAYMENT_TITLE',
    'PAYMENT_DESCRIPTION',
    'PAYMENT_CONTACT_INFO',
    'PSF_SPEEDTYPE',
    'PSF_ACCT_NUMBER',
    'TECHNICAL_CONTACT',
    'REQUEST_CONTACT',
]

DEBUG = False
DATABASES['default'] = env.db('DATABASE_URL')
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME = env('AWS_SES_REGION_NAME')
AWS_SES_REGION_ENDPOINT = env('AWS_SES_REGION_ENDPOINT')
DEFAULT_FROM_EMAIL = 'no-reply@workshops.qiime2.org'
SERVER_EMAIL = 'no-reply@workshops.qiime2.org'
EMAIL_HOST = 'workshops.qiime2.org'
EMAIL_SUBJECT_PREFIX = '[workshops.qiime2.org] '

# BUSINESS LOGIC
ADMINS = env('ADMINS',
             cast=lambda entry: [record.split(',') for record in entry.split(';')])
LMID = env.str('LMID')
PAYMENT_URL = env.str('PAYMENT_URL')
PAYMENT_TITLE = env.str('PAYMENT_TITLE')
PAYMENT_DESCRIPTION = env.str('PAYMENT_DESCRIPTION')
PAYMENT_CONTACT_INFO = env.str('PAYMENT_CONTACT_INFO')
PSF_SPEEDTYPE = env.str('PSF_SPEEDTYPE')
PSF_ACCT_NUMBER = env.str('PSF_ACCT_NUMBER')
TECHNICAL_CONTACT = env.str('TECHNICAL_CONTACT')
REQUEST_CONTACT = env.str('REQUEST_CONTACT')
