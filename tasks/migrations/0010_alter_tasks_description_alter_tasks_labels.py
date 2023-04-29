# Generated by Django 4.2 on 2023-04-28 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0002_alter_labels_options'),
        ('tasks', '0009_alter_tasks_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='labels',
            field=models.ManyToManyField(blank=True, to='labels.labels', verbose_name='Labels'),
        ),
    ]