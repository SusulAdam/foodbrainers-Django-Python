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
    # Manytomanyfiled tworzry nowa tabele w django jako powiazanie miedzy dwoma tabelami
    cuisines = models.ManyToManyField(Cuisine)
    # logo?
    opening_hours = models.CharField(max_length=20)
    min_order_amount = models.PositiveIntegerField(default=0)
    # wspiera wprowadzenie pustego pola (blank=True)

    # menu = models.ManyToManyField("Course", blank=True, related_name='restaurant_set')


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
    # domyślnie tabela pośredniczaca jest sama tworzna, jeśli chcemy konkretnie ja stworzyć robiby to za pomoca through
    # zawsze stworzy sei tabela posrednicznaca i by sie samo zrobilo order i course (a wie o tym, że order to Order, a course to Course), dzieki temu ze dalismy through mozemy dodac dodkowa ilosc quantity
    courses = models.ManyToManyField(Course, through='OrderEntry')
    amount = models.PositiveIntegerField(default=0)
    delivery_cost = models.PositiveIntegerField(default=0)
    delivery = models.CharField(max_length=50)


class OrderEntry(models.Model):
    # musza być odwolanie w lewo i  w prawo na dodatkowo dwie kolumny, order i course !
    #order w ktorym zamowieniu zwiekszaniu
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # a kuchnia to jaka kuchnie zwiekszamy
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
