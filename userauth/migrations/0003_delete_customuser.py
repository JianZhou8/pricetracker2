# Generated by Django 4.2.5 on 2023-10-30 03:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("userauth", "0002_remove_customuser_groups_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CustomUser",
        ),
    ]
