from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.

class User(AbstractUser):
    birthday = models.DateField(blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    image = models.URLField(default="https://i.imgur.com/obUumGz.jpg")
    def name(self): return self.first_name +" "+ self.last_name
    def age(self):
        try: return int((date.today() - self.birthday).days/365)
        except: return None



class Category(models.Model):
    name = models.CharField(max_length=15)
    def __str__(self): return self.name


class Event(models.Model):
    title = models.CharField(max_length=140)
    description = models.CharField(max_length=300, default="No description given")
    location = models.CharField(max_length=30)
    date = models.DateField()
    duration = models.TimeField()
    organizer = models.CharField(max_length=40)
    venue = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    price = models.IntegerField()
    trending = models.BooleanField(default=False)
    image = models.URLField(default="https://i.imgur.com/l0Q1Cqj.jpg")

    def __str__(self):
        return self.title + " " + self.location

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " For " + str(self.event)


