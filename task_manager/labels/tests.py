from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.users.models import User


class LabelTest(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']

    def test_create_label(self):
        new_label = {
            'name': 'flask',
        }
        response = self.client.get(reverse('labels:create'))
        self.assertRedirects(response, reverse('login'), 302)
        auth_user = User.objects.last()
        self.client.force_login(auth_user)
        response = self.client.get(reverse('labels:create'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('labels:create'), new_label, follow=True)
        self.assertRedirects(response, reverse('labels:labels'), 302)
        new_label = Label.objects.last()
        self.assertTrue(new_label.name == 'flask')

    def test_update_label(self):
        update_label = Label.objects.last()
        auth_user = User.objects.last()
        response = self.client.get(reverse('labels:update', args=(update_label.id,)))
        self.assertRedirects(response, reverse('login'), 302)
        self.client.force_login(auth_user)
        response = self.client.get(reverse('labels:update', args=(update_label.id,)))
        self.assertEqual(response.status_code, 200)
        new_label = {
            'name': 'work',
        }
        response = self.client.post(reverse('labels:update', args=(update_label.id,)), new_label, follow=True)
        self.assertRedirects(response, reverse('labels:labels'), 302)
        new_label = Label.objects.last()
        self.assertTrue(new_label.name == 'work')

    def test_delete_label(self):
        delete_label = Label.objects.last()
        auth_user = User.objects.last()
        response = self.client.get(reverse('labels:delete', args=(delete_label.id,)))
        self.assertRedirects(response, reverse('login'), 302)
        self.client.force_login(auth_user)
        response = self.client.get(reverse('labels:delete', args=(delete_label.id,)))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('labels:delete', args=(delete_label.id,)), follow=True)
        '''Label can not be deleted because it is in use.'''
        self.assertRedirects(response, reverse('labels:labels'), 302)
        label = Label.objects.last()
        self.assertTrue(label.name == 'bugs')
        '''Found all tasks where the label is used. And deleted them'''
        tasks = Task.objects.filter(labels=label.pk)
        for task in tasks:
            self.client.post(reverse('tasks:delete', args=(task.id,)), follow=True)
        '''Now you can test delete of a label'''
        response = self.client.post(reverse('labels:delete', args=(label.id,)), follow=True)
        self.assertRedirects(response, reverse('labels:labels'), 302)
        label = Label.objects.last()
        self.assertEqual(label.name, 'Python')
