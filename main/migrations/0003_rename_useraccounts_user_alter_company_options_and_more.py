# Generated by Django 4.2.4 on 2024-06-01 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_alter_department_department_name"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UserAccounts",
            new_name="User",
        ),
        migrations.AlterModelOptions(
            name="company",
            options={"ordering": ["id"]},
        ),
        migrations.AlterModelOptions(
            name="department",
            options={"ordering": ["company"]},
        ),
        migrations.AlterModelOptions(
            name="employee",
            options={"ordering": ["id"]},
        ),
    ]
