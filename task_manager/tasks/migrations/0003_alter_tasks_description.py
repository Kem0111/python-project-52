# Generated by Django 4.2 on 2023-04-25 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_tasks_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
    ]
