# QIIME 2 Workshops

[![Build Status](https://travis-ci.org/qiime2/workshops.svg?branch=master)](https://travis-ci.org/qiime2/workshops)
[![Coverage Status](https://coveralls.io/repos/github/qiime2/workshops/badge.svg?branch=master)](https://coveralls.io/github/qiime2/workshops?branch=master)

Django App for QIIME 2 workshops

## Development Setup

    # Default buildpack runtime is Python 3.6
    $ conda create -n workshops.qiime2.org python=3.6
    $ conda activate workshops.qiime2.org
    $ pip install -r requirements/local.txt
    $ createdb qiime2-workshops
    $ python manage.py migrate
    $ python manage.py runserver

## Basic Commands

Creating a **superuser account**:

    $ python manage.py createsuperuser

## Deploying to Dokku

    dokku config:set $APPNAME \
        ADMIN_URL=`openssl rand -base64 32` \
        SECRET_KEY=`openssl rand -base64 64` \
        SETTINGS_MODULE='config.settings.production' \
        ALLOWED_HOSTS='.qiime2.org,workshops.qiime2.org' \
        ADMINS='x,x@x.com;y,y@y.com' \
        LMID=YOUR_LMID \
        PAYMENT_URL=YOUR_PAYMENT_URL \
        PAYMENT_TITLE=YOUR_PAYMENT_TITLE \
        PAYMENT_DESCRIPTION=YOUR_PAYMENT_DESCRIPTION \
        PAYMENT_CONTACT_INFO=YOUR_PAYMENT_CONTACT_INFO \
        PSF_SPEEDTYPE=YOUR_PSF_SPEEDTYPE \
        PSF_ACCT_NUMBER=YOUR_PSF_ACCT_NUMBER \
        AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID \
        AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY \
        AWS_SES_REGION_NAME=YOUR_AWS_SES_REGION_NAME \
        AWS_SES_REGION_ENDPOINT=YOUR_AWS_REGION_ENDPOINT

    git push dokku master
    dokku run python manage.py migrate
    dokku run python manage.py check --deploy
    dokku run python manage.py createsuperuser

## NAU Notes

- Test EBusiness server is not accessible outside of NAU - must test locally
