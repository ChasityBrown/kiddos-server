# Generated by Django 4.0.3 on 2022-03-15 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kiddosapi', '0004_alter_kid_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='kid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='kiddosapi.kid'),
        ),
    ]
