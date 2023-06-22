# Generated by Django 4.2.2 on 2023-06-22 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="signuptype",
            field=models.CharField(
                choices=[("H.O", "House Owner"), ("T", "Tenants")], max_length=200
            ),
        ),
    ]
