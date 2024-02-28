from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass
    

class File(models.Model):
    name = models.CharField(max_length=100)
    postedBy = models.ForeignKey(User, related_name='posteds', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    postedAt = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=100)
    userPermition = models.BooleanField(default=False)
    allowedUsers = models.ManyToManyField(User, related_name='allowedFiles')
    downloadsCount = models.IntegerField(default=0)

class MessageCommonInfos(models.Model):
    message = models.CharField(max_length=200)
    sendAt = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    class Meta:
        abstract = True
    
class Message(MessageCommonInfos):
    caller = models.ForeignKey(User, related_name='sends', on_delete=models.CASCADE, null=True)
    reciver = models.ForeignKey(User,related_name='messages',on_delete=models.CASCADE)

class RequestMessage(MessageCommonInfos):
    caller = models.ForeignKey(User, related_name='requestsSends', on_delete=models.CASCADE, null=True)
    reciver = models.ForeignKey(User,related_name='requestsMessages',on_delete=models.CASCADE)
    file  = models.ForeignKey(File, on_delete=models.CASCADE)
    
        