# Generated by Django 4.0.3 on 2022-03-11 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiddosapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetup',
            name='attendees',
            field=models.ManyToManyField(related_name='attending', through='kiddosapi.KidMeetUp', to='kiddosapi.kid'),
        ),
    ]
