import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class RegistrationForm(forms.Form):

    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    name = forms.CharField(label=_("Registration Name"), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))

    def clean_username(self):
        try:
            user = User.objects.\
                   get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.\
              ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


def enforce_file_extension(file_name, allowed_file_types):
    if not file_name:
        return False

    file_name = file_name.split('.')

    if isinstance(file_name, list) and len(file_name) > 0:
        extension = file_name[-1]

        if extension in allowed_file_types:
            return True

    return False

FILE_UPLOAD_EXTENSIONS = ['csv']

class FileUploadForm(forms.Form):
    '''
        Form for uploading file
    '''
    upload_file = forms.FileField(label="Upload File",
                                  required=True, help_text=
                                  ("CSV file to be processed"))

    def clean_upload_file(self):
        '''
            Enforce file type
            :return:
        '''
        curr_file = self.cleaned_data['upload_file']

        if not enforce_file_extension(curr_file.name, FILE_UPLOAD_EXTENSIONS):
            raise forms.ValidationError('Invalid file format. '
                                        'Can only upload file types {}'.\
                                         format(' '.join(FILE_UPLOAD_EXTENSIONS)))
        if curr_file._size > 10*1024*1024:
            raise forms.ValidationError("File size is greater than 10 MB")
