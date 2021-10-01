from django.db import models


class Food(models.Model):

    Name = models.CharField(max_length=500)
    EatenOn = models.DateTimeField()
    Calories = models.IntegerField(blank=True)
    Qty = models.IntegerField()
    User = models.CharField(max_length=20)
    def __str__(self):
        return self.name


class Event(models.Model):

    Description = models.CharField(max_length=200)
    HappenedOn = models.DateTimeField()
    User = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Energy(models.Model):

    Description = models.CharField(max_length=200)
    ExertedOn = models.DateTimeField()
    Duration = models.IntegerField()
    Units = models.CharField(max_length=100)
    User = models.CharField(max_length=20)
    def __str__(self):
        return self.name


