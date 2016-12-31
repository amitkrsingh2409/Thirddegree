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
&nbsp;&nbsp;&nbsp;&nbsp;    'default': {<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        'ENGINE': 'django.db.backends.postgresql',<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        'NAME': 'thirddegree_db',<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        'USER': 'amitsingh',<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        'PASSWORD': 'thirddegree',<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        'HOST': '',<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        'PORT': '',<br />
&nbsp;&nbsp;&nbsp;&nbsp;   }<br />
}<br />
<br />
$ pip install psycopg2<br />

