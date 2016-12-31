# Thirddegree
File management system for clients

Steps to setup ThirdDegree

$ virtualenv -p /usr/bin/python3.4 /home/delhivery/JaguarPaw/vir3.4<br />
$ pip install Django<br />
$ django-admin startproject thirddegree<br />
$ cd thirddegree<br />
$ python manage.py runserver<br />
<br />
Database setup<br />
$ sudo -i -u postgres<br />
$ psql<br />
$ CREATE USER amitsingh WITH PASSWORD 'thirddegree';<br />
$ CREATE DATABASE thirddegree_db OWNER amitsingh;<br />
<br />
DATABASES = {<br />
    'default': {<br />
        'ENGINE': 'django.db.backends.postgresql',<br />
        'NAME': 'thirddegree_db',<br />
        'USER': 'amitsingh',<br />
        'PASSWORD': 'thirddegree',<br />
        'HOST': '',<br />
        'PORT': '',<br />
    }<br />
}<br />
<br />
$ pip install psycopg2<br />

