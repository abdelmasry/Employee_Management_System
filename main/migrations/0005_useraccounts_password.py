# Generated by Django 4.2.4 on 2024-06-01 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_rename_user_useraccounts"),
    ]

    operations = [
        migrations.AddField(
            model_name="useraccounts",
            name="password",
            field=models.CharField(default="password", max_length=64),
        ),
    ]
