# Generated by Django 4.0.6 on 2022-09-16 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('labels', '0001_initial'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='executors', to=settings.AUTH_USER_MODEL, verbose_name='Executor'),
        ),
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, to='labels.label', verbose_name='Labels'),
        ),
    ]