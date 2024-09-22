# Generated by Django 4.2.15 on 2024-09-22 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0021_remove_usersanswer_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='result',
            field=models.CharField(choices=[('OK', 'The program is guaranteed to output:'), ('CE', 'The program has a compilation error'), ('UD', 'The program is (or may be) undefined'), ('US', 'The program is unspecified / implementation defined')], default='OK', max_length=2),
        ),
        migrations.AlterField(
            model_name='usersanswer',
            name='result',
            field=models.CharField(choices=[('OK', 'The program is guaranteed to output:'), ('CE', 'The program has a compilation error'), ('UD', 'The program is (or may be) undefined'), ('US', 'The program is unspecified / implementation defined')], default='OK', max_length=2),
        ),
    ]
