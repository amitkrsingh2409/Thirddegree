"""thirddegree URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib.auth.views import login
from django.conf.urls import include, url
from thirddegree.views import *

urlpatterns = [
    url(r'^$', login, {'template_name': 'registration/login.html'}),
    url(r'^logout/$', logout_page),
    url(r'^create_dir/$', create_directory),
    url(r'^dir/(\d+)/$', edit_directory, name='edit_directory'),
    url(r'^dir/delete/(\d+)/$', delete_directory),
    url(r'^file/delete/(\d+)/(?P<name>[\w.@+-]+)/$', delete_file),
    url(r'^accounts/login/$', login), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home/$', home),
]
