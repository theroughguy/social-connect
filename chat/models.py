from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique=True,null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True,default='avatar.svg')

    #avatar
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []






class Topic(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name




class room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    #host
    #topic

    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(User,related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created','-updated']

class Messages(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Room = models.ForeignKey(room,on_delete=models.CASCADE)
    body = models.TextField(null=True)


    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-updated','created']

    def __str__(self):
        return self.body[0:50]