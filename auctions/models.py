from django.contrib.auth.models import AbstractUser
from django.db import models

import datetime


class User(AbstractUser):
    pass

class Listing(models.Model):
    item = models.CharField(max_length=64)
    price = models.FloatField()
    timestamp = datetime.datetime.now()
    image = models.ImageField(default= None, max_length = 100, upload_to='images/')
    details =  models.CharField(max_length=300)
    category = models.CharField(max_length=40)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=None)

    def __str__(self):
        return f"{self.item}"
    
class Watchlist(models.Model):
    watchlist = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None)    
    item = models.CharField(max_length=64)
    price = models.FloatField()
    timestamp = datetime.datetime.now()
    details =  models.CharField(max_length=300)
    category = models.CharField(max_length=40)
    user = models.ManyToManyField(User, blank= True, related_name="watchlists")

    def __str__(self):
        return f"{self.item}"
    
class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None) 
    bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.bid}"

class Winner(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None)
    winner = models.CharField(max_length=40, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.user}"

class Comments(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE) 
    text = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
       return f"{self.text}"

class Category(models.Model):
    category = models.CharField(max_length=40)
    listings = models.ManyToManyField(Listing, blank=True, related_name="categories")
    
    def __str__(self):
       return f"{self.category}"