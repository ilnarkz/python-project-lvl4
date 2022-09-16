from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class StatusTest(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']

    def test_create_status(self):
        new_status = {
            'name': 'Not done',
        }
        response = self.client.get(reverse('statuses:create'))
        self.assertRedirects(response, reverse('login'), 302)
        auth_user = User.objects.last()
        self.client.force_login(auth_user)
        response = self.client.get(reverse('statuses:create'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('statuses:create'), new_status, follow=True)
        self.assertRedirects(response, reverse('statuses:statuses'), 302)
        new_user = Status.objects.last()
        self.assertTrue(new_user.name == 'Not done')

    def test_update_status(self):
        update_status = Status.objects.last()
        auth_user = User.objects.last()
        response = self.client.get(reverse('statuses:update', args=(update_status.id,)))
        self.assertRedirects(response, reverse('login'), 302)
        self.client.force_login(auth_user)
        response = self.client.get(reverse('statuses:update', args=(update_status.id,)))
        self.assertEqual(response.status_code, 200)
        new_status = {
            'name': 'Done',
        }
        response = self.client.post(reverse('statuses:update', args=(update_status.id,)), new_status, follow=True)
        self.assertRedirects(response, reverse('statuses:statuses'), 302)
        new_status = Status.objects.last()
        self.assertTrue(new_status.name == 'Done')

    def test_delete_status(self):
        delete_status = Status.objects.last()
        auth_user = User.objects.last()
        response = self.client.get(reverse('statuses:delete', args=(delete_status.id,)))
        self.assertRedirects(response, reverse('login'), 302)
        self.client.force_login(auth_user)
        response = self.client.get(reverse('statuses:delete', args=(delete_status.id,)))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('statuses:delete', args=(delete_status.id,)), follow=True)
        '''Status can not be deleted because it is in use.'''
        self.assertRedirects(response, reverse('statuses:statuses'), 302)
        status = Status.objects.last()
        self.assertTrue(status.name == 'new')
        '''Found all tasks where the status is used. And deleted them'''
        tasks = Task.objects.filter(status=status.id)
        for task in tasks:
            self.client.post(reverse('tasks:delete', args=(task.id,)), follow=True)
        '''Now you can test delete of a status'''
        response = self.client.post(reverse('statuses:delete', args=(delete_status.id,)), follow=True)
        self.assertRedirects(response, reverse('statuses:statuses'), 302)
        status = Status.objects.last()
        self.assertTrue(status.name == 'completed')
