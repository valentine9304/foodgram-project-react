# Generated by Django 4.2.4 on 2023-08-09 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0004_alter_ingredients_options_alter_recipes_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recipes",
            name="Ingredients",
        ),
        migrations.AlterField(
            model_name="recipes",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор рецепта",
            ),
        ),
        migrations.AlterField(
            model_name="recipes",
            name="cooking_time",
            field=models.PositiveSmallIntegerField(verbose_name="Время готовки"),
        ),
        migrations.AlterField(
            model_name="recipes",
            name="name",
            field=models.CharField(
                db_index=True, max_length=200, verbose_name="Имя рецепта"
            ),
        ),
        migrations.AlterField(
            model_name="recipes",
            name="tags",
            field=models.ManyToManyField(to="recipes.tags", verbose_name="Тэги"),
        ),
        migrations.AlterField(
            model_name="recipes",
            name="text",
            field=models.TextField(verbose_name="Описание"),
        ),
        migrations.AddField(
            model_name="recipes",
            name="ingredients",
            field=models.ManyToManyField(
                through="recipes.RecipesIngredients",
                to="recipes.ingredients",
                verbose_name="Используемые ингредиенты",
            ),
        ),
    ]