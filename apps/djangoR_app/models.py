from __future__ import unicode_literals
from django.core.validators import MaxValueValidator
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def register(self, postData):
        password = postData['password']
        hashed_pw = bcrypt.hashpw(password.encode(encoding="utf-8", errors="strict"), bcrypt.gensalt())
        #First User to Register is Admin Level, else Normal level
        user = UserName.objects.create(
            name = postData['name'],
            user_name = postData['user_name'],
            password = hashed_pw
        )
        return {
            'user':user
            # 'message': "Thank You For Registering!"
            }

    def login(self, postData):
        password = postData['password']
        user = UserName.objects.get(user_name = postData['user_name'])
        return {
            'user':user
            # 'message' : "You Have Successfully Logged In!"
            }

# Create your models here.
class UserName(models.Model):
    name = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.TextField(max_length=100)
    description = models.TextField(max_length=1000)
    travelDate_from = models.DateField()
    travelDate_to = models.DateField()
    user = models.ForeignKey(UserName, related_name="trips_scheduled")
    all_users = models.ManyToManyField(UserName, related_name="all_trips")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
