# Generated by Django 4.0.3 on 2022-03-17 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiddosapi', '0005_alter_game_kid'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='fave_game',
            field=models.ManyToManyField(related_name='fave_games', through='kiddosapi.FaveGame', to='kiddosapi.kid'),
        ),
        migrations.AddField(
            model_name='room',
            name='fave_rooms',
            field=models.ManyToManyField(related_name='fave_rooms', through='kiddosapi.FaveRoom', to='kiddosapi.kid'),
        ),
    ]
