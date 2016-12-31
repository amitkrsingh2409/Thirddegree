from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.validators import MaxValueValidator
from rest_framework.authtoken.models import Token
from pymongo import MongoClient
from pymongo import MongoReplicaSetClient

from thirddegree.app_settings import DIRECTORIES_CACHE

class Client(models.Model):
    '''
        Client models for saving all client related information
    '''
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50, db_index=True, unique=True)
    bandwidth = models.IntegerField(default=0, validators=[
            MaxValueValidator(10*1024*1024)
    ])
    storage = models.IntegerField(default=0, validators=[
        MaxValueValidator(1*1024*1024)
    ])
    def get_rest_token(self):
        '''
         Get the rest token
        '''
        if hasattr(self, 'user'):
            user = self.user
            try:
                token = user.auth_token.key
            except:
                instance, created = Token.objects.get_or_create(user=user)
                token = instance.key
            return token
        return None

    def get_all_directories(self, typ='dict'):
        '''
            Get list of all directories mapped to Client
        '''
        key = '{0}{1}_{2}'.\
              format(DIRECTORIES_CACHE, self.name.replace(' ', '_'), typ)
        result = cache.get(key,  []) or []
        if not result:
            cl_dirs = ClientDirectories.objects.filter(client=self)
            if typ == 'dict':
                result = [{'id': cl_dir.id, 'name': cl_dir.name} for cl_dir in cl_dirs]
            else:
                result = [str(cl_dir.id) for cl_dir in cl_dirs]
            cache.set(key, result)
        return result


class ClientDirectories(models.Model):
    '''
        List of directories mapped to a client
    '''
    client = models.ForeignKey(Client)
    name = models.CharField(max_length=50, db_index=True, unique=True)

    def client_mapped(self):
        '''
         Get the client mapped to a particular directory
        '''
        if hasattr(self, 'client'):
            client = self.client
            return client.name
        return None


class MongoConnection(object):
    '''
        Mongo Connection - uses singleton class
    '''

    def __init__(self, timeout=2* 60*1000):
        self.host = 'localhost'
        self.port = 27017
        self.database = 'thirddegree'
        self.user = 'amit.singh'
        self.password = 'thirddegree'
        self.timeout = timeout
        self.connection = dict()

    def set_connection(self):
        '''
            Creates connection to MOGODB_URI
        '''
        self.connection = MongoClient(
            host=self.host, port=self.port,
            connectTimeoutMS=self.timeout
        )

    def get_connection(self):
        if not self.connection:
            self.set_connection()
        return self.connection
