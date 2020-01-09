from datetime import date

from django.urls import reverse
from django.db import models

from menu.managers import ActiveMenuManager


class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateField(default=date.today)
    expiration_date = models.DateField(blank=True, null=True)

    objects = models.Manager()
    active_menus = ActiveMenuManager()

    def __str__(self):
        return self.season

    def get_absolute_url(self):
        return reverse('menu_detail', args=[self.id])


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL)
    created_date = models.DateField(default=date.today)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item_detail', args=[self.id])


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
