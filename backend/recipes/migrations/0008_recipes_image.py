# Generated by Django 4.2.4 on 2023-08-09 16:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0007_rename_ingridient_recipesingredients_ingredient"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipes",
            name="image",
            field=models.ImageField(blank=True, upload_to="media/"),
        ),
    ]