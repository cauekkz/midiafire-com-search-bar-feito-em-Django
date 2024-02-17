from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass
    

class File(models.Model):
    name = models.CharField(max_length=100)
    postedBy = models.ForeignKey(User, related_name='posteds', on_delete=models.CASCADE,default='the account no longer exists')
    file = models.FileField(upload_to='uploads/')
    postedAt = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=100)
    userPermition = models.BooleanField(default=False)
    allowedUsers = models.ManyToManyField(User, related_name='allowedFiles')
    downloadsCount = models.IntegerField(default=0)
    messages = models.ManyToManyField(User, related_name='myRequests')

    
