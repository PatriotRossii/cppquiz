# Generated by Django 2.2.17 on 2020-12-19 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0017_auto_20200922_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='last_viewed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
