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
?ts=4    'default': {<br />
?ts=6        'ENGINE': 'django.db.backends.postgresql',<br />
?ts=6        'NAME': 'thirddegree_db',<br />
?ts=6        'USER': 'amitsingh',<br />
?ts=6        'PASSWORD': 'thirddegree',<br />
?ts=6        'HOST': '',<br />
?ts=6        'PORT': '',<br />
?ts=4    }<br />
}<br />
<br />
$ pip install psycopg2<br />

