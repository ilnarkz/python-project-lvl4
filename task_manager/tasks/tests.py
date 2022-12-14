from django.test import TestCase
from django.urls import reverse

from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskTest(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']

    def test_create_task(self):
        new_task = {
            'name': 'Not done',
            'description': 'Not done project',
            'status': 1,
            'labels': [1, 2, 3],
            'executor': 2
        }
        response = self.client.get(reverse('tasks:create'))
        self.assertRedirects(response, reverse('login'), 302)
        auth_user = User.objects.last()
        self.client.force_login(auth_user)
        response = self.client.get(reverse('tasks:create'))
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.count()
        self.assertEqual(tasks, 3)
        response = self.client.post(
            reverse('tasks:create'),
            new_task,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks:tasks'), 302)
        tasks = Task.objects.count()
        self.assertEqual(tasks, 4)
        task = Task.objects.last()
        self.assertTrue(task.name == 'Not done')
        self.assertTrue(task.description == 'Not done project')
        self.assertTrue(task.status.name == "At work")
        self.assertTrue(task.executor.username == 'claude_math')
        self.assertTrue(task.author.username == auth_user.username)
        self.assertEqual(task.labels.count(), 3)
        for t in task.labels.values():
            self.assertTrue(t['name'] in ['Django', 'Python', 'bugs'])

    def test_update_task(self):
        update_task = Task.objects.last()
        auth_user = User.objects.last()
        response = self.client.get(reverse('tasks:update', args=(update_task.id,)))
        self.assertRedirects(response, reverse('login'), 302)
        self.client.force_login(auth_user)
        response = self.client.get(reverse('tasks:update', args=(update_task.id,)))
        self.assertEqual(response.status_code, 200)
        new_task = {
            'name': 'Create project',
            'description': 'Create django project',
            'status': 2,
            'labels': [1, 3],
            'executor': 2
        }
        response = self.client.post(
            reverse('tasks:update', args=(update_task.id,)),
            new_task,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks:tasks'), 302)
        new_task = Task.objects.last()
        self.assertTrue(new_task.name == 'Create project')
        self.assertTrue(new_task.description == 'Create django project')
        self.assertTrue(new_task.status.name == 'completed')
        self.assertTrue(new_task.executor.username == "claude_math")
        self.assertTrue(new_task.author.username == 'alan_machine')
        self.assertEqual(new_task.labels.count(), 2)
        for t in new_task.labels.values():
            self.assertTrue(t['name'] in ['Django', 'bugs'])

    def test_delete_task(self):
        delete_task = Task.objects.last()
        auth_user = User.objects.get(pk=2)
        response = self.client.get(reverse('tasks:delete', args=(delete_task.id,)))
        self.assertRedirects(response, reverse('login'), 302)
        self.client.force_login(auth_user)
        response = self.client.get(reverse('tasks:delete', args=(delete_task.id,)))
        self.assertRedirects(response, reverse('tasks:tasks'), 302)
        auth_user = User.objects.get(pk=3)
        self.client.force_login(auth_user)
        response = self.client.get(reverse('tasks:delete', args=(delete_task.id,)))
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.count()
        self.assertEqual(tasks, 3)
        response = self.client.post(
            reverse('tasks:delete', args=(delete_task.id,)),
            follow=True
        )
        self.assertRedirects(response, reverse('tasks:tasks'), 302)
        tasks = Task.objects.count()
        self.assertEqual(tasks, 2)
        task = Task.objects.last()
        self.assertTrue(task.name == "Project")
        self.assertTrue(task.description == "Create project")
        self.assertTrue(task.status.name == 'completed')
        self.assertTrue(task.executor.username == "claude_math")
        self.assertTrue(task.author.username == "claude_math")
        self.assertEqual(task.labels.count(), 2)
        for t in task.labels.values():
            self.assertTrue(t['name'] in ['Django', 'Python'])

    def test_filter_list(self):
        auth_user = User.objects.last()
        self.client.force_login(auth_user)
        tasks = Task.objects.all()
        filter_by_empty_fields = TaskFilter({}, queryset=tasks)
        self.assertEqual(len(filter_by_empty_fields.qs), 3)
        filter_by_status = TaskFilter({'status': 1}, queryset=tasks)
        self.assertEqual(len(filter_by_status.qs), 1)
        self.assertEqual(filter_by_status.qs.get(status=1).name, 'Docs')
        filter_by_executor = TaskFilter({'executor': 2}, queryset=tasks)
        self.assertEqual(len(filter_by_executor.qs), 2)
        for task_qs in filter_by_executor.qs:
            self.assertTrue(task_qs.name in ['Project', 'Testing'])
        filter_by_labels = TaskFilter({'labels': 3}, queryset=tasks)
        self.assertEqual(len(filter_by_labels.qs), 2)
        for task_qs in filter_by_labels.qs:
            self.assertTrue(task_qs.name in ['Docs', 'Testing'])
