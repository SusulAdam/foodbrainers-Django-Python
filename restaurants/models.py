from django.db import models
from django.contrib.auth.models import User


class Cuisine(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    cuisines = models.ManyToManyField(Cuisine)
    opening_hours = models.CharField(max_length=20)
    min_order_amount = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.PositiveIntegerField()
    is_spicy = models.BooleanField()
    is_vegan = models.BooleanField()
    is_glutenfree = models.BooleanField()


    restaurant = models.ForeignKey(Restaurant, null=True, on_delete=models.CASCADE , related_name='menu')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    courses = models.ManyToManyField(Course, through='OrderEntry')
    amount = models.PositiveIntegerField(default=0)
    delivery_cost = models.PositiveIntegerField(default=0)
    delivery = models.CharField(max_length=50)


class OrderEntry(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
