# Generated by Django 4.2 on 2023-04-24 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuses',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='name'),
        ),
    ]