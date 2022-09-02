from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import User


class UserTest(TestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.user1 = get_user_model().objects.get(pk=1)
        self.user2 = get_user_model().objects.get(pk=2)
        self.user3 = get_user_model().objects.get(pk=3)

    def test_create_user(self):
        new_user = {
            'first_name': 'John',
            'last_name': 'Nash',
            'username': 'NashOfficial',
            'password1': 'cyh2UTJrjexWUD2Akwo6',
            'password2': 'cyh2UTJrjexWUD2Akwo6'
        }
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('create'), new_user, follow=True)
        self.assertRedirects(response, '/login/', 302)
        new_user = User.objects.last()
        self.assertTrue(new_user.username == 'NashOfficial')
        self.assertTrue(new_user.check_password('cyh2UTJrjexWUD2Akwo6'))
        self.assertTrue(new_user.first_name == 'John')
        self.assertTrue(new_user.last_name == 'Nash')
        self.assertTrue(new_user.id == 4)

    def test_update_user(self):
        update_user = User.objects.last()
        self.client.force_login(update_user)
        response = self.client.get(reverse('update', args=(update_user.id,)))
        self.assertEqual(response.status_code, 200)
        new_user = {
            'first_name': 'John',
            'last_name': 'Nash',
            'username': 'NashOfficial',
            'password1': 'cyh2UTJrjexWUD2Akwo6',
            'password2': 'cyh2UTJrjexWUD2Akwo6'
        }
        response = self.client.post(reverse('update', args=(update_user.id,)), new_user, follow=True)
        self.assertRedirects(response, '/users/', 302)
        new_user = User.objects.last()
        self.assertTrue(new_user.username == 'NashOfficial')
        self.assertTrue(new_user.check_password('cyh2UTJrjexWUD2Akwo6'))
        self.assertTrue(new_user.first_name == 'John')
        self.assertTrue(new_user.last_name == 'Nash')
        self.assertTrue(new_user.id == 3)

    def test_delete_user(self):
        delete_user = User.objects.last()
        self.client.force_login(delete_user)
        response = self.client.get(reverse('delete', args=(delete_user.id,)))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('delete', args=(delete_user.id,)), follow=True)
        self.assertRedirects(response, '/', 302)
        user = User.objects.last()
        self.assertFalse(user.username == 'NashOfficial')
