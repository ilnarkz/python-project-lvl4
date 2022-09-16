# Generated by Django 4.0.6 on 2022-09-16 20:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('statuses', '0001_initial'),
        ('labels', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created date')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='authors', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('executor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='executors', to=settings.AUTH_USER_MODEL, verbose_name='Executor')),
                ('labels', models.ManyToManyField(to='labels.label', verbose_name='Labels')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='statuses.status', verbose_name='Status')),
            ],
        ),
    ]
