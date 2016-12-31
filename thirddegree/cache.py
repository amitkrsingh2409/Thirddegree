from django.core.cache import cache
from django.core.exceptions import ValidationError
from thirddegree.app_settings import CLIENT_FILES_STRUCTURE

def fetch_client_files(client_name, directory=None):
    '''
        Redis cache to fetch client files
    '''
    key = '{0}{1}'.format(CLIENT_FILES_STRUCTURE, client_name.replace(' ', '_'))
    if directory:
        return cache.get(key, {}).get(directory) or {}
    return cache.get(key, {}) or {}


def dump_client_files(client, directory, file_name, path_name, file_size):
    '''
        Dump unique file in client
    '''
    if client.storage - int(file_size) > 1024*1024:
        raise ValidationError('Max storage exceeded for given client')
    key = '{0}{1}'.format(CLIENT_FILES_STRUCTURE, client.name.replace(' ', '_'))
    all_files = fetch_client_files(client.name)
    directories = client.get_all_directories(typ='list')
    for d in directories:
        if all_files.get(d, {}).get(file_name) and d != directory:
            raise ValidationError('File already exists for the given client')
    # Unique file good to go
    if not all_files.get(directory):
        all_files[directory] = {}
    if not all_files.get(directory, {}).get(file_name):
        all_files[directory][file_name] = {}
    all_files[directory][file_name] = {'path': path_name, 'size': int(file_size)}
    cache.set(key, all_files)
    prev_bandwidth = client.bandwidth
    prev_storage = client.storage
    client.bandwidth = prev_bandwidth + int(file_size)
    client.storage = prev_storage + int(file_size)
    client.save()
