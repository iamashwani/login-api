
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from decimal import Decimal
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from random import choice
# def random_image():
#     directory = os.path.join(settings.BASE_DIR, 'static')
#     files = os.listdir(directory)
#     images = [file for file in files if os.path.isfile(os.path.join(directory, file))]
#     rand = choice(images)
#     return rand
class User(models.Model):
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)  
    #logo_path = models.CharField(max_length=200)
    logo = models.ImageField(upload_to ="profile/", null=True,blank =True)
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
    
    
    
    
    # @receiver(post_save, sender=logo)
    # def create_or_update_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         User.objects.create(logo=instance)
    #     instance.logo.save()