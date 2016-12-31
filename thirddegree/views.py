from thirddegree.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from thirddegree.models import Client, ClientDirectories
from thirddegree.cache import dump_client_files, fetch_client_files
from thirddegree.app_settings import DIRECTORIES_CACHE, CLIENT_FILES_STRUCTURE

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            Client.objects.create(name=form.cleaned_data['name'], user=user)
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    return render(request,
        'registration/register.html', {'form': form}
    )

def register_success(request):
    return render(request,
        'registration/success.html'
    )

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def home(request):
    user = request.user
    directories = user.client.get_all_directories()
    return render(request,
        'home.html',
        { 'user': user,
         'directories': directories}
    )

@login_required
@csrf_protect
def create_directory(request):
    user = request.user
    if request.method == 'POST':
        client = user.client
        name = request.POST.get('name')
        key = key = '{0}{1}_{2}'.\
              format(DIRECTORIES_CACHE, client.name.replace(' ', '_'), 'dict')
        cl_dir = ClientDirectories(client=client, name=name)
        cl_dir.save()
        cache.delete(key)
        return HttpResponseRedirect('/home/')
    return render(request,
        'create_directory.html', {'user': user}
    )


@login_required
def edit_directory(request, pkey):
    user = request.user
    cl_dir = ClientDirectories.objects.get(pk=pkey)
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = request.FILES['upload_file']
            file_size = upload_file.size
            filename = u'/tmp/{0}'.format(upload_file.name)
            try:
                dump_client_files(user.client, str(pkey), \
                                  upload_file.name, filename, file_size)
            except ValidationError as err:
                files = fetch_client_files(user.client.name, directory=str(pkey))
                return render(request,
                    'edit_directory.html', {'user': user, \
                    'dir': cl_dir, 'form': FileUploadForm(),
                    'error': str(err.message),
                    'files': files.keys()}
                )
            with open(filename, 'wb+') as f:
                f.write(upload_file.read())
    else:
        form = FileUploadForm()
    files = fetch_client_files(user.client.name, directory=str(pkey))
    return render(request,
        'edit_directory.html', {'user': user, 'dir': cl_dir, 'form': form,
        'files': files.keys()}
    )


@login_required
def delete_directory(request, pkey):
    user = request.user
    cl_dir = ClientDirectories.objects.get(pk=pkey)
    cl_dir.delete()
    key = '{0}{1}_{2}'.\
          format(DIRECTORIES_CACHE, user.client.name.replace(' ', '_'), 'dict')
    cache.delete(key)
    all_files = fetch_client_files(user.client.name)
    all_files.pop(str(pkey), None)
    key1 = '{0}{1}'.format(CLIENT_FILES_STRUCTURE, user.client.name.replace(' ', '_'))
    cache.set(key1, all_files)
    return HttpResponseRedirect('/home/')


@login_required
def delete_file(request, pkey, name):
    user = request.user
    prev_storage = user.client.storage
    all_files = fetch_client_files(user.client.name)
    fileparams = all_files.get(str(pkey), {}).pop(name, {})
    key1 = '{0}{1}'.format(CLIENT_FILES_STRUCTURE, user.client.name.replace(' ', '_'))
    cache.set(key1, all_files)
    user.client.storage = prev_storage - (fileparams.get('size', 0))
    user.client.save()
    url = reverse('edit_directory', args=[pkey])
    return HttpResponseRedirect(url)
