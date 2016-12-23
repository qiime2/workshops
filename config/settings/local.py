# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

"""
Local development settings
"""

from .base import *  # noqa: F403


SECRET_KEY = env('DJANGO_SECRET_KEY',  # noqa: F405
                 default='j@^@b1)4k4t!$z5si3e*#r=26x-sgfas(!!qb=el8*t12xv8su')

DEBUG = env.bool('DJANGO_DEBUG', default=True)  # noqa: F405
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa: F405

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',  # noqa: F405
                    default='django.core.mail.backends.console.EmailBackend')

INSTALLED_APPS += ['debug_toolbar']  # noqa: F405
MIDDLEWARE += ['payments.middleware.PatchedDebugToolbarMiddleware']  # noqa: F405
DEBUG_TOOLBAR_PATCH_SETTINGS = False
