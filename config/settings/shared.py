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
MAILING_ADDRESS = env.str('MAILING_ADDRESS', 'Northern Arizona University<br>'
                          'The Pathogen and Microbiome Institute<br>'
                          'PO Box 4073<br>'
                          'Flagstaff, AZ 86011 USA')
BANK_INFO = env.str('BANK_INFO', '<h2 style="color:#F00; padding-bottom:-15px">WIRE TRANSFER PAYMENTS</h2>'
                    '<dl class="list">'
                    '<dt>Wire Routing Transit # (RTN/ABA):</dt>'
                    '<dd>121000248</dd>'
                    '<dt>Bank Name:</dt>'
                    '<dd>'
                    'Wells Fargo Bank, N.A.<br>'
                    '420 Montgomery<br>'
                    'San Francisco, CA 94104'
                    '</dd>'
                    '<dt>Beneficiary Account #:</dt>'
                    '<dd>4126665298</dd>'
                    '<dt>Beneficiary:</dt>'
                    '<dd>Northern Arizona University, Non Repetitive Wires/1910040F25</dd>'
                    '<dt>SWIFT/BIC:</dt>'
                    '<dd>WFBIUS6S</dd>'
                    '<dt>CHIPS Participant:</dt>'
                    '<dd>ABA 0407</dd>'
                    '</dl>')
