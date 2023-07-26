# Generated by Django 4.2 on 2023-07-26 08:53

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
                choices=[("House Owner", "House Owner"), ("Tenant", "Tenant")],
                default="H.O",
                max_length=200,
            ),
        ),
    ]
