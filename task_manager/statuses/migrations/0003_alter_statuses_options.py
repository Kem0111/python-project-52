# Generated by Django 4.2 on 2023-04-26 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0002_alter_statuses_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statuses',
            options={'ordering': ['-created_at'], 'verbose_name': 'Statuses', 'verbose_name_plural': 'Statuses'},
        ),
    ]
