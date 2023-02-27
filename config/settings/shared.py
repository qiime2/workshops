# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os

import environ


env = environ.Env()


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROJ_DIR = os.path.join(BASE_DIR, 'workshops')
SECRET_KEY = '1%k!0ogj-o(1r&b%9kmvndggr8+z1kl74!p87*l@fg1&mtjv+#'
DEBUG = env('DEBUG', default=True)
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'markdownx',

    'workshops.payments',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJ_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'workshops.payments.context_processors.contact_info',
            ],
        },
    },
]
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'qiime2-workshops',
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
# Note that these paths should use Unix-style forward slashes, even on Windows
STATICFILES_DIRS = ['%s/static' % PROJ_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
APPEND_SLASH = True  # This is the default, but just want make it explicit
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# BUSINESS LOGIC
ADMINS = env('ADMINS', default=[('x', 'x@x.com')],
             cast=lambda entry: [record.split(',') for record in entry.split(';')])
LMID = env.str('LMID', '1234')
PAYMENT_URL = env.str('PAYMENT_URL', 'http://www.example.com')
PAYMENT_TITLE = env.str('PAYMENT_TITLE', 'test')
PAYMENT_DESCRIPTION = env.str('PAYMENT_DESCRIPTION', 'test')
PAYMENT_CONTACT_INFO = env.str('PAYMENT_CONTACT_INFO', 'EXAMPLE GROUP\n'
                                                       'example@example.com')
PSF_SPEEDTYPE = env.str('PSF_SPEEDTYPE', '0000')
PSF_ACCT_NUMBER = env.str('PSF_ACCT_NUMBER', '0000')
TECHNICAL_CONTACT = env.str('TECHNICAL_CONTACT', 'Problems with '
                            'purchasing a ticket? '
                            '<a href="mailto:test@test.com">'
                            'Contact us.</a>')
REQUEST_CONTACT = env.str('REQUEST_CONTACT', 'Interested in hosting or '
                          'attending an official QIIME 2 Workshop? '
                          '<a href="mailto:test@test.com">'
                          'Contact us.</a>')
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000
