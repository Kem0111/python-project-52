# Generated by Django 4.2 on 2023-04-25 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_remove_tasks_description_tasks_discription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='discription',
        ),
        migrations.AddField(
            model_name='tasks',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
    ]
