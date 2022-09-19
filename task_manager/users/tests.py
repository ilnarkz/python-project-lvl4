from django.test import TestCase
from django.urls import reverse

from task_manager.tasks.models import Task
from task_manager.users.models import User


class UserTest(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']

    def test_create_user(self):
        new_user = {
            'first_name': 'John',
            'last_name': 'Nash',
            'username': 'NashOfficial',
            'password1': 'cyh2UTJrjexWUD2Akwo6',
            'password2': 'cyh2UTJrjexWUD2Akwo6'
        }
        response = self.client.get(reverse('users:create'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=new_user['username']))
        response = self.client.post(
            reverse('users:create'),
            new_user,
            follow=True
        )
        self.assertRedirects(response, reverse('login'), 302)
        new_user = User.objects.last()
        self.assertTrue(new_user.username == 'NashOfficial')
        self.assertTrue(new_user.check_password('cyh2UTJrjexWUD2Akwo6'))
        self.assertTrue(new_user.first_name == 'John')
        self.assertTrue(new_user.last_name == 'Nash')
        self.assertTrue(new_user.id == 4)

    def test_update_user(self):
        update_user = User.objects.last()
        self.client.force_login(update_user)
        response = self.client.get(reverse('users:update', args=(update_user.id,)))
        self.assertEqual(response.status_code, 200)
        new_user = {
            'first_name': 'John',
            'last_name': 'Nash',
            'username': 'NashOfficial',
            'password1': 'cyh2UTJrjexWUD2Akwo6',
            'password2': 'cyh2UTJrjexWUD2Akwo6'
        }
        self.assertFalse(User.objects.filter(username=new_user['username']))
        response = self.client.post(
            reverse('users:update', args=(update_user.id,)),
            new_user,
            follow=True)
        self.assertRedirects(response, reverse('users:users'), 302)
        new_user = User.objects.last()
        self.assertTrue(new_user.username == 'NashOfficial')
        self.assertTrue(new_user.check_password('cyh2UTJrjexWUD2Akwo6'))
        self.assertTrue(new_user.first_name == 'John')
        self.assertTrue(new_user.last_name == 'Nash')
        self.assertTrue(new_user.id == 3)

    def test_delete_user(self):
        delete_user = User.objects.last()
        self.assertFalse(delete_user.username == 'claude_math')
        self.client.force_login(delete_user)
        response = self.client.get(reverse('users:delete', args=(delete_user.id,)))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse('users:delete', args=(delete_user.id,)),
            follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(
            str(messages[0]),
            "Невозможно удалить пользователя, потому что он используется"
        )
        self.assertRedirects(response, reverse('users:users'), 302)
        user = User.objects.last()
        self.assertTrue(user.username == "alan_machine")
        '''Found all tasks where the user is used. And deleted them'''
        tasks = Task.objects.filter(author=delete_user.id)
        for task in tasks:
            self.client.post(
                reverse('tasks:delete', args=(task.id,)),
                follow=True
            )
        tasks = Task.objects.filter(executor=delete_user.id)
        for task in tasks:
            self.client.post(
                reverse('tasks:delete', args=(task.id,)),
                follow=True
            )
        '''Now you can test delete of a user'''
        response = self.client.post(
            reverse('users:delete', args=(delete_user.id,)),
            follow=True
        )
        self.assertRedirects(response, reverse('users:users'), 302)
        user = User.objects.last()
        self.assertTrue(user.username == "claude_math")
