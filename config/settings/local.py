"""
Local development settings
"""

from .base import * # gross but is the best for now


SECRET_KEY = env('DJANGO_SECRET_KEY',
                 default='j@^@b1)4k4t!$z5si3e*#r=26x-sgfas(!!qb=el8*t12xv8su')

DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')
