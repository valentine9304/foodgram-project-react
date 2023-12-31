# Generated by Django 4.2.4 on 2023-08-15 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0008_recipes_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredients",
            name="measurement_unit",
            field=models.CharField(
                help_text="Введите единицу измерения",
                max_length=200,
                verbose_name="Единица измерения",
            ),
        ),
        migrations.AlterField(
            model_name="ingredients",
            name="name",
            field=models.CharField(
                db_index=True,
                help_text="Введите название ингредиента",
                max_length=200,
                verbose_name="Название ингридента",
            ),
        ),
        migrations.AlterField(
            model_name="recipes",
            name="author",
            field=models.ForeignKey(
                help_text="Введите имя автора рецепта",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор рецепта",
            ),
        ),
        migrations.AlterField(
            model_name="recipes",
            name="cooking_time",
            field=models.PositiveSmallIntegerField(
                help_text="Укажите время приготовления рецепта в минутах",
                verbose_name="Время готовки",
            ),
        ),
        migrations.AlterField(
            model_name="recipes",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Загрузите изображение",
                upload_to="images/",
                verbose_name="Изображение",
            ),
        ),
        migrations.AlterField(
            model_name="recipes",
            name="ingredients",
            field=models.ManyToManyField(
                help_text="Перечислите используемые ингредиенты",
                through="recipes.RecipesIngredients",
                to="recipes.ingredients",
                verbose_name="Используемые ингредиенты",
            ),
        ),
        migrations.AlterField(
            model_name="recipes",
            name="name",
            field=models.CharField(
                db_index=True,
                help_text="Введите название рецепта",
                max_length=200,
                verbose_name="Название рецепта",
            ),
        ),
        migrations.AlterField(
            model_name="recipes",
            name="tags",
            field=models.ManyToManyField(
                help_text="Укажите приём пищи (можно несколько)",
                to="recipes.tags",
                verbose_name="Приём пищи",
            ),
        ),
        migrations.AlterField(
            model_name="recipes",
            name="text",
            field=models.TextField(
                help_text="Опишите приготовление рецепта", verbose_name="Описание"
            ),
        ),
    ]
