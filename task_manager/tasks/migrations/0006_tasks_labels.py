# Generated by Django 4.2 on 2023-04-26 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0005_remove_tasks_discription_tasks_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='labels',
            field=models.ManyToManyField(blank=True, to='labels.labels'),
        ),
    ]
