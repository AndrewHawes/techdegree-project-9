from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from menu import forms
from menu.models import Menu, Item, Ingredient


def create_ingredients(ingredients):
    return [Ingredient.objects.create(name=ingredient) for ingredient in ingredients]


def create_item(name, chef, ingredients, description='It’s similar to food.'):
    item = Item.objects.create(name=name, chef=chef, description=description)
    item.ingredients.set(create_ingredients(ingredients))

    return item


def create_menu(season, items, expiration_date=None):
    menu = Menu.objects.create(season=season, expiration_date=expiration_date)
    menu.items.set(items)

    return menu


class MenuTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username='zorbert', password='fish?hi!')
        self.client.force_login(self.user)

        cheesecake_ingredients = [
            'cream cheese', 'sugar', 'butter', 'graham crackers',
            'sour cream', 'eggs', 'lemon zest', 'canned tuna'
        ]
        pizza_ingredients = ['mozzarella', 'pesto', 'dough', 'horse fur', 'crayons']

        self.cheesecake = create_item(
            name="Cheesecake",
            chef=self.user,
            ingredients=cheesecake_ingredients
        )
        self.pizza = create_item(
            name='Pizza',
            chef=self.user,
            ingredients=pizza_ingredients
        )

        self.menu = create_menu('Summer', [self.pizza, self.cheesecake])
        self.old_menu = create_menu('Expired Menu', [self.pizza], '2003-12-21')

    def test_menu_list(self):
        url = reverse('menu_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['menus'],
            ['<Menu: Summer>'],
        )

    def test_menu_detail(self):
        url = reverse('menu_detail', args=(self.menu.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print('menu', response.context['menu'])
        print(type(response.context['menu']))
        self.assertEqual(
            response.context['menu'].season,
            'Summer',
        )

    def test_item_detail(self):
        url = reverse('item_detail', args=(self.pizza.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['item'].name,
            'Pizza'
        )

    def test_menu_form_validates_expiration_date_not_past(self):
        data = {
            'season': 'Summer 2007',
            'items': [self.pizza.id],
            'expiration_date': '2007-08-21'}
        form = forms.MenuForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {'expiration_date': ['Expiration date cannot be in the past.']}
        )

    def test_menu_form_validates_date_format(self):
        data = {
            'season': 'Summer 2007',
            'items': [self.pizza.id],
            'expiration_date': '12-11-2050'}
        form = forms.MenuForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {'expiration_date': ['Enter a valid date.']}
        )

    def test_menu_form_accepts_valid_date_format(self):
        data = {
            'season': 'Summer 2007',
            'items': [self.pizza.id],
            'expiration_date': '12/11/2050'}
        form = forms.MenuForm(data)
        self.assertTrue(form.is_valid())

    def test_menu_create_view(self):
        self.client.force_login(self.user)
        url = reverse('menu_new')
        data = {
            'season': 'Summer 2007',
            'items': [self.cheesecake.id],
            'expiration_date': '12/11/2050'}

        response = self.client.post(url, data)
        menu = Menu.objects.get(season=data['season'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/menu/{menu.id}/')

    def test_item_edit_view(self):
        self.client.force_login(self.user)
        url = reverse('item_edit', kwargs={'pk': self.cheesecake.pk})
        data = {
            'name': self.cheesecake.name,
            'description': 'What??',
            'chef': self.cheesecake.chef.id,
            'created_date': self.cheesecake.created_date,
            'standard': self.cheesecake.standard,
            'ingredients': list(self.cheesecake.ingredients.values_list('id', flat=True))
        }

        response = self.client.post(url, data=data)
        self.cheesecake.refresh_from_db()
        self.assertEqual(self.cheesecake.description, 'What??')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/menu/item/{self.cheesecake.id}/')

