# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

"""
Production settings
"""

from .base import *  # noqa 403


SECRET_KEY = env('DJANGO_SECRET_KEY')  # noqa: F405
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS += ['djangosecure']  # noqa: F405

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(  # noqa: F405
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_FRAME_DENY = env.bool("DJANGO_SECURE_FRAME_DENY", default=True)  # noqa: F405
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(  # noqa: F405
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)  # noqa: F405


ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['workshops.qiime.org'])  # noqa: F405


TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa: F405
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader', ]),
    ]


DATABASES['default'] = env.db("DATABASE_URL")  # noqa: F405


DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',  # noqa: F405
                         default='QIIME Workshops Admin '
                         '<noreply@qiime2.org>')
EMAIL_BACKEND = 'anymail.backends.sparkpost.EmailBackend'
SPARKPOST_API_KEY = env('SPARKPOST_API_KEY')  # noqa: F405
EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default='[qiime workshops] ')  # noqa: F405
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)  # noqa: F405


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'mail_admins'],
            'propagate': True
        }
    }
}


ADMIN_URL = env('DJANGO_ADMIN_URL')  # noqa: F405

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

ADMINS = env('ADMINS', cast=list_of_tuples)  # noqa: F405

# App-specific business logic
LMID = env.str('LMID')  # noqa: F405
PAYMENT_URL = env.str('PAYMENT_URL')  # noqa: F405
PAYMENT_TITLE = env.str('PAYMENT_TITLE')  # noqa: F405
PAYMENT_DESCRIPTION = env.str('PAYMENT_DESCRIPTION')  # noqa: F405
PAYMENT_CONTACT_INFO = env.str('PAYMENT_CONTACT_INFO')  # noqa: F405
PAYMENT_CERT_BUNDLE = env.str('PAYMENT_CERT_BUNDLE')  # noqa: F405
PSF_SPEEDTYPE = env.str('PSF_SPEEDTYPE')  # noqa: F405
PSF_ACCT_NUMBER = env.str('PSF_ACCT_NUMBER')  # noqa: F405
TECHNICAL_CONTACT = env.str('TECHNICAL_CONTACT')  # noqa: F405
