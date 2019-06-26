from django.test import TestCase
from django.urls import reverse

from menu.models import Menu, Item, Ingredient
from menu.forms import MenuForm
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


# coverage run --source='.' manage.py test myapp

class AllModelTests(TestCase):
    def setUp(self):
        form = UserCreationForm(data={
            'id': 10,
            'username': 'miro',
            'password1': 'Qwertyuiop164964+',
            'password2': 'Qwertyuiop164964+'
        })
        form.save()
        self.user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )

    def test_models_success(self):
        now = timezone.now()
        future = timezone.now() + timedelta(days=10)
        ingredients_data_one = {
            'name': 'chocolate'
        }
        ingredient_one = Ingredient.objects.create(**ingredients_data_one)
        ingredients_data_two = {
            'name': 'vanilla'
        }
        ingredient_two = Ingredient.objects.create(**ingredients_data_two)
        item_data = {
            'name': 'chocolate cake',
            'description': 'cake',
            'chef': self.user,
            'created_date': now,
            'standard': True,
        }
        item = Item.objects.create(**item_data)
        item.ingredients.set([ingredient_one, ingredient_two])
        menu_data = {
            'season': 'winter',
            'created_date': now,
            'expiration_date': future
        }
        menu = Menu.objects.create(**menu_data)
        menu.items.set([item])
        self.assertEqual(menu_data['season'], menu.season)
        self.assertEqual(menu_data['created_date'], menu.created_date)
        self.assertEqual(menu_data['expiration_date'], menu.expiration_date)
        # chef
        self.assertEqual(self.user, menu.items.get(id=1).chef)
        # chocolate cake
        self.assertEqual(item, menu.items.get(id=1))
        # chocolate
        self.assertEqual(ingredient_one, menu.items.get(
            id=1).ingredients.get(id=1))
        # vanilla
        self.assertEqual(ingredient_two, menu.items.get(
            id=1).ingredients.get(id=2))


class MenuFormTests(TestCase):
    def setUp(self):
        form = UserCreationForm(data={
            'id': 10,
            'username': 'miro',
            'password1': 'Qwertyuiop164964+',
            'password2': 'Qwertyuiop164964+'
        })
        form.save()
        self.user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        self.now = timezone.now()
        self.future = timezone.now() + timedelta(days=10)
        ingredients_data_one = {
            'name': 'chocolate'
        }
        self.ingredient_one = Ingredient.objects.create(**ingredients_data_one)
        ingredients_data_two = {
            'name': 'vanilla'
        }
        self.ingredient_two = Ingredient.objects.create(**ingredients_data_two)
        item_data = {
            'name': 'chocolate cake',
            'description': 'cake',
            'chef': self.user,
            'created_date': self.now,
            'standard': True,
        }
        self.item = Item.objects.create(**item_data)
        self.item.ingredients.set([self.ingredient_one, self.ingredient_two])
        menu_data = {
            'season': 'winter',
            'created_date': self.now,
            'expiration_date': self.future
        }
        self.menu = Menu.objects.create(**menu_data)
        self.menu.items.set([self.item])

    def test_new_menuform_valid(self):
        form = MenuForm(data={
            'season': 'winter',
            'items': Item.objects.all(),
            'expiration_date': '05/05/2015'
        })
        self.assertTrue(form.is_valid())

    def test_new_menuform_invalid_date_format(self):
        form = MenuForm(data={
            'season': 'winter',
            'items': Item.objects.all(),
            'expiration_date': '2015-05-08'
        })
        self.assertFalse(form.is_valid())


class MenuViewsTests(TestCase):
    def setUp(self):
        form = UserCreationForm(data={
            'id': 10,
            'username': 'miro',
            'password1': 'Qwertyuiop164964+',
            'password2': 'Qwertyuiop164964+'
        })
        form.save()
        self.user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        self.now = timezone.now()
        self.future = timezone.now() + timedelta(days=10)
        ingredients_data_one = {
            'name': 'chocolate'
        }
        self.ingredient_one = Ingredient.objects.create(**ingredients_data_one)
        ingredients_data_two = {
            'name': 'vanilla'
        }
        self.ingredient_two = Ingredient.objects.create(**ingredients_data_two)
        item_data = {
            'name': 'chocolate cake',
            'description': 'cake',
            'chef': self.user,
            'created_date': self.now,
            'standard': True,
        }
        self.item = Item.objects.create(**item_data)
        self.item.ingredients.set([self.ingredient_one, self.ingredient_two])
        menu_data = {
            'season': 'winter',
            'created_date': self.now,
            'expiration_date': self.future
        }
        self.menu = Menu.objects.create(**menu_data)
        self.menu.items.set([self.item])

        self.client.force_login(self.user)

    def test_Menu_menu_list(self):
        response = self.client.get(
            reverse('menu:menu_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/list_all_current_menus.html')
        self.assertContains(response, 'winter')

    def test_Menu_menu_detail(self):
        response = self.client.get(
            reverse('menu:menu_detail', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/menu_detail.html')
        self.assertContains(response, 'chocolate cake')

    def test_Menu_item_detail(self):
        response = self.client.get(
            reverse('menu:item_detail', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/detail_item.html')
        self.assertContains(response, 'cake')
        self.assertContains(response, 'miro')

    def test_Menu_item_detail_error(self):
        response = self.client.get(
            reverse('menu:item_detail', kwargs={'pk': 2}))

        self.assertEqual(response.status_code, 404)

    def test_Menu_menu_new(self):
        response = self.client.post(
            reverse('menu:menu_new'), data={
                'season': 'summer',
                'items': ['1'],
                'expiration_date': '10/10/2016'
            })
        self.assertEqual(response.status_code, 302)

    def test_Menu_menu_edit(self):
        response = self.client.post(
            reverse('menu:menu_edit', kwargs={'pk': 1}), {
                'season': 'spring',
                'items': ['1'],
                'expiration_date': '05/05/2015'
            })
        self.assertEqual(response.status_code, 302)

    def test_Menu_menu_edit_invalid(self):
        response = self.client.post(
            reverse('menu:menu_edit', kwargs={'pk': 1}), {
                'season': 'spring',
                'items': ['1'],
                'expiration_date': '2015-10-10'
            })
        # redirects if form is valid
        self.assertEqual(response.status_code, 200)
