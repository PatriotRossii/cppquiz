# Generated by Django 1.11.15 on 2018-09-17 10:45


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0012_auto_20180427_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='retraction_message',
            field=models.TextField(blank=True, default=b''),
        ),
    ]
