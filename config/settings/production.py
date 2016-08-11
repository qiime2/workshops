# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

"""
Production settings
"""

from .base import * # gross but is the best for now


SECRET_KEY = env('DJANGO_SECRET_KEY')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS += ['djangosecure']

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
SECURE_FRAME_DENY = env.bool("DJANGO_SECURE_FRAME_DENY", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)


ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['workshops.qiime.org'])


TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader', ]),
    ]


DATABASES['default'] = env.db("DATABASE_URL")


DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
                         default='QIIME Workshops Admin <noreply@workshops.qiime.org>')
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = env('DJANGO_MAILGUN_API_KEY')
MAILGUN_SERVER_NAME = env('DJANGO_MAILGUN_SERVER_NAME')
EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default='[qiime workshops] ')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)


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


ADMIN_URL = env('DJANGO_ADMIN_URL')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# App-specific business logic
LMID = env.str('LMID')
PAYMENT_URL = env.str('PAYMENT_URL')
PAYMENT_TITLE = env.str('PAYMENT_TITLE')
PAYMENT_DESCRIPTION = env.str('PAYMENT_DESCRIPTION')
PAYMENT_CONTACT_INFO = env.str('PAYMENT_CONTACT_INFO')
PAYMENT_CERT_BUNDLE = env.str('PAYMENT_CERT_BUNDLE')
PSF_SPEEDTYPE = env.str('PSF_SPEEDTYPE')
PSF_ACCT_NUMBER = env.str('PSF_ACCT_NUMBER')
