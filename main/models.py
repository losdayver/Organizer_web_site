from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    text = models.TextField()
    startTime = models.DateTimeField()
    tag = models.CharField(max_length=40)

class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    text = models.TextField()
    color = models.TextField(max_length=7)
    lastModifiedTime = models.DateTimeField(auto_now=True)