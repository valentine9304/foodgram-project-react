# Generated by Django 4.2.4 on 2023-09-05 16:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0013_alter_ingredients_options_recipes_pub_date_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="shoppingcart",
            name="unique_cart",
        ),
        migrations.AddConstraint(
            model_name="shoppingcart",
            constraint=models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_cart"
            ),
        ),
    ]
