# Thirddegree
File management system for clients

Steps to setup ThirdDegree

$ virtualenv -p /usr/bin/python3.4 /home/delhivery/JaguarPaw/vir3.4
$ pip install Django
$ django-admin startproject thirddegree
$ cd thirddegree
$ python manage.py runserver

Database setup
$ sudo -i -u postgres
$ psql
$ CREATE USER amitsingh WITH PASSWORD 'thirddegree';
$ CREATE DATABASE thirddegree_db OWNER amitsingh;

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'thirddegree_db',
        'USER': 'amitsingh',
        'PASSWORD': 'thirddegree',
        'HOST': '',
        'PORT': '',
    }
}

$ pip install psycopg2

