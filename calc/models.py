from django.db import models

# Create your models here.
class User(models.Model):
    pic= models.ImageField(upload_to="userpic")


class feedback_entry(models.Model):
    name=models.CharField(max_length=7)
    feedback=models.CharField(max_length=700)
    userid=models.CharField(max_length=10)
