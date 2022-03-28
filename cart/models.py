from django.db import models
# from django.contrib.auth.models import User
# Create your models here.
from django.utils.crypto import get_random_string
import os
import random
from django.core.files import File  # you need this somewhere
import urllib
import urllib.parse
import urllib, os
# from urlparse import urlparse
from urllib.parse import urlparse
import urllib.request
import json
import requests
# from django.core.files.storage import FileSystemStorage
# fs = FileSystemStorage(location='/media/photos')

class User(models.Model):
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    logo = models.ImageField(upload_to ='profile/')
    logo_path = models.CharField(max_length=200)
    profile_id = models.CharField(max_length=200)

    
    # upload_path='absolute path'
    # def save(self, *args, **kwargs):
    #     if self.logo_path:
    #         file_save_dir = self.upload_path
    #         filename = urlparse(self.logo_path).path.split('/')[-1]
    #         urllib.request.urlretrieve(self.logo_path, os.path.join(file_save_dir, filename))
    #         self.image = os.path.join(file_save_dir, filename)
    #         self.logo_path = ''
    #     super(User, self).save()

