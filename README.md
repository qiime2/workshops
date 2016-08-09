# QIIME Workshops

[![Build Status](https://travis-ci.org/jakereps/qiime-workshops.svg?branch=master)](https://travis-ci.org/jakereps/qiime-workshops)

Django App for QIIME workshop payments

## Development Setup

    $ pyvenv venv
    $ echo "MANIFEST_URL=some_data_url" > .env
    $ source venv/bin/activate
    $ pip install -r requirements/local.txt
    $ python manage.py migrate
    $ python manage.py runserver

## Basic Commands

Creating a **superuser account**:

    $ python manage.py createsuperuser

## Deploying to Heroku

    heroku create --buildpack https://github.com/heroku/heroku-buildpack-python

    heroku addons:create heroku-postgresql:hobby-dev
    heroku pg:backups schedule --at '02:00 America/Phoenix' DATABASE_URL
    heroku pg:promote DATABASE_URL

    heroku config:set DJANGO_ADMIN_URL=`openssl rand -base64 32`
    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 64`
    heroku config:set DJANGO_SETTINGS_MODULE='config.settings.production'
    heroku config:set DJANGO_ALLOWED_HOSTS='.herokuapp.com'

    heroku config:set DJANGO_MAILGUN_SERVER_NAME=YOUR_MALGUN_SERVER
    heroku config:set DJANGO_MAILGUN_API_KEY=YOUR_MAILGUN_API_KEY

    heroku config:set LMID=YOUR_LMID
    heroku config:set PAYMENT_URL=YOUR_PAYMENT_URL
    heroku config:set PAYMENT_TITLE=YOUR_PAYMENT_TITLE
    heroku config:set PAYMENT_DESCRIPTION=YOUR_PAYMENT_DESCRIPTION
    heroku config:set PAYMENT_CONTACT_INFO=YOUR_PAYMENT_CONTACT_INFO
    heroku config:set PAYMENT_CERT_BUNDLE=YOUR_PAYMENT_CERT_BUNDLE

    heroku config:set PSF_SPEEDTYPE=YOUR_PSF_SPEEDTYPE
    heroku config:set PSF_ACCT_NUMBER=YOUR_PSF_ACCT_NUMBER

    heroku config:set PYTHONHASHSEED=random
    heroku config:set DJANGO_ADMIN_URL=\^somelocation/

    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py check --deploy
    heroku run python manage.py createsuperuser
    heroku open
