# Generated by Django 4.2.4 on 2023-08-09 15:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0006_alter_recipesingredients_recipe"),
    ]

    operations = [
        migrations.RenameField(
            model_name="recipesingredients",
            old_name="ingridient",
            new_name="ingredient",
        ),
    ]