from django.db import models


class User(models.Model):
    twitter_handle = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

class Bribe(models.Model):
    message = models.CharField(max_length=200)
    briber = models.ForeignKey(User, related_name='briber')
    bribee = models.ForeignKey(User, related_name='bribee')

class Charity(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    givinglab_id = models.CharField(max_length=100)
    logo_url = models.CharField(max_length=300)

