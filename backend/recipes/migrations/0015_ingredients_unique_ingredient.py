# Generated by Django 4.2.4 on 2023-09-05 16:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0014_remove_shoppingcart_unique_cart_and_more"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="ingredients",
            constraint=models.UniqueConstraint(
                fields=("name", "measurement_unit"), name="unique_ingredient"
            ),
        ),
    ]
