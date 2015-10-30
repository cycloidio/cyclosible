[![Stories in Ready](https://badge.waffle.io/cycloidio/cyclosible.png?label=ready&title=Ready)](https://waffle.io/cycloidio/cyclosible)
Cyclosible
==========

[![Build Status](https://travis-ci.org/cycloidio/cyclosible.svg)](https://travis-ci.org/cycloidio/cyclosible)
[![Coverage Status](https://coveralls.io/repos/cycloidio/cyclosible/badge.svg?branch=master&service=github)](https://coveralls.io/github/cycloidio/cyclosible?branch=master)


Cyclosible is a project backed by [Cycloid] in order to manage Ansible with a REST API.

The goal of Cyclosible is to be a lightweight application opensourced as a free alternative to Ansible Tower.

Cyclosible is used internally at [Cycloid] to let our customers use their own CI and interact with our deployment stack.

Technologies used
-----------------

Cyclosible is built upon these technologies:
* [Django]
* [Django REST Framework]
* [Celery]
* [Redis]
* [S3]

Prerequisite
------------

### Install REDIS

To start with Cyclosible, you will need to install redis. For this we suggest to create a [redis docker container]

### Create Virtual Environment

First, install virtualenv:
```bash
sudo pip install virtualenv
sudo pip install virtualenvwrapper
```

Then, create the virtualenv:
```bash
mkvirtualenv cyclosible27 --no-site-packages -p /usr/bin/python2.7
```

I suggest here to install python 2.7 as ansible does not support python 3 yet.

Now, to work in your virtual environment, you can enable it with:
```bash
workon cyclosible27
```

### Install required packages

You will need to clone this repository. Then you will be able to install the requirements:
```bash
pip install -r requirements.txt
```
    
### Configure the S3 bucket

Actually the S3 bucket is mandatory. In the future we will try to make it optional or provide a plugin system to write your own storage.

You will need to activate the Website Hosting on your S3 bucket, and apply this permission (where cycloid-cyclosible is the name of your bucket):
```json
{
  "Version":"2012-10-17",
  "Statement":[{
    "Sid":"PublicReadGetObject",
        "Effect":"Allow",
      "Principal": "*",
      "Action":["s3:GetObject"],
      "Resource":["arn:aws:s3:::cycloid-cyclosible/*"
      ]
    }
  ]
}
```

Configure the application
-------------------------

For this step, you will have to edit the cyclosible/Cyclosible/settings.py file, and configure these parameters:
* BROKER_URL = 'redis://localhost:6379/0'
* CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
* CELERY_TIMEZONE = 'Europe/Paris'
* SECRET_KEY = 'random string'
* PLAYBOOK_PATH = "/home/ansible_playbook_path/"
* S3_BUCKET = "cycloid-cyclosible"
* S3_ACCESS_KEY = "XXXXXXXXXXX"
* S3_SECRET_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

Before starting the application, we need to create the database. You can also configure the DATABASE settings, by default it will create a SQLite3 database.
Please refer to the django website (link is above this parameter) to configure it correctly.

Then, apply the schema:
```bash
<cyclosible_path>/manage.py migrate
```

It will populate the database. Then you need to create a superuser:
```bash
<cyclosible_path>/manage.py createsuperuser
```
    
Start the application
---------------------

The best way to run the application on production is to use [supervisord].

There are 3 applications to start :

- This one will start the webserver (DEV mode):
```bash
<cyclosible_path>/manage.py runserver
```

- This one will start the worker which will run the playbook:
```bash
<cyclosible_path>/manage.py celery worker
```

- This one will check if there are some tasks ton run on crontabs (actually optional):
```bash
<cyclosible_path>/manage.py celery beat
```

Now you should be able to connect on the admin interface: `http://<yourip>:8000/admin/`

Development
-----------

All unit tests are run with tox:
```bash
pip install tox
```
    
Then, run tox at the root of the project:
```bash
tox
```
    

[Cycloid]: http://www.cycloid.io
[Ansible Tower]: http://www.ansible.com/tower
[redis docker container]: https://hub.docker.com/_/redis/
[Django]: https://www.djangoproject.com/
[Django REST Framework]: http://www.django-rest-framework.org/
[Celery]: http://www.celeryproject.org/
[Redis]: http://redis.io/
[S3]: https://aws.amazon.com/fr/s3/
[supervisord]: http://supervisord.org/