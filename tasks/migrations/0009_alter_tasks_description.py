# Generated by Django 4.2 on 2023-04-28 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_alter_tasks_options_alter_tasks_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
    ]
