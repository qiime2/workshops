# ----------------------------------------------------------------------------
# Copyright (c) 2016-2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os

import environ


from .shared import (
    BASE_DIR,
    PROJ_DIR,
    SECRET_KEY,
    DEBUG,
    ALLOWED_HOSTS,
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
    EMAIL_BACKEND,
    DATA_UPLOAD_MAX_NUMBER_FIELDS,

    # BUSINESS LOGIC
    ADMINS,
    LMID,
    PAYMENT_URL,
    PAYMENT_TITLE,
    PAYMENT_DESCRIPTION,
    PAYMENT_CONTACT_INFO,
    PSF_SPEEDTYPE,
    PSF_ACCT_NUMBER,
    TECHNICAL_CONTACT,
    REQUEST_CONTACT,
)


environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


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


MIDDLEWARE.extend([
    'debug_toolbar.middleware.DebugToolbarMiddleware'
])
INTERNAL_IPS = ['127.0.0.1', 'localhost']
INSTALLED_APPS = ['whitenoise.runserver_nostatic', *INSTALLED_APPS, 'debug_toolbar']
