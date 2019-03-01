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
]

DEBUG = False
DATABASES['default'] = env.db('DATABASE_URL')
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
EMAIL_BACKEND = 'sparkpost.django.email_backend.SparkPostEmailBackend'
SPARKPOST_API_KEY = env('SPARKPOST_API_KEY')
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
