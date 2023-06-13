from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=40)
    text = models.TextField()
    startTime = models.DateTimeField(null=False)
    tag = models.CharField(max_length=40)

class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=40, null=False)
    text = models.TextField()
    color = models.CharField(max_length=7, null=False)
    lastModifiedTime = models.DateTimeField(auto_now=True, null=False)

class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=40, null=False)
    status = models.SmallIntegerField(null=False)