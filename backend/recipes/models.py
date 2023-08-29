from django.db import models
from users.models import User


class Tags(models.Model):
    """Тэги для Рецептов."""

    GREEN = "#09DB4F"
    ORANGE = "#E26C2D"
    PURPLE = "#B813D1"
    COLOR_TAG = [
        (GREEN, "Зеленый"),
        (ORANGE, "Оранжевый"),
        (PURPLE, "Фиолетовый"),
    ]
    name = models.CharField(max_length=200, verbose_name="Название")
    color = models.CharField(
        max_length=7,
        verbose_name="Цвет в HEX",
        default=GREEN,
        choices=COLOR_TAG,
    )
    slug = models.SlugField(
        max_length=200, unique=True, verbose_name="Уникальный слаг"
    )

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        ordering = ("id",)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """Ингредиенты для рецептов."""

    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name="Название ингридента",
        help_text="Введите название ингредиента",
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Единица измерения",
        help_text="Введите единицу измерения",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("id",)

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """Рецепты."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
        help_text="Введите имя автора рецепта",
    )
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name="Название рецепта",
        help_text="Введите название рецепта",
    )
    image = models.ImageField(
        upload_to="images/",
        blank=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение",
    )
    text = models.TextField(
        verbose_name="Описание",
        help_text="Опишите приготовление рецепта",
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through="RecipesIngredients",
        verbose_name="Используемые ингредиенты",
        help_text="Перечислите используемые ингредиенты",
    )
    tags = models.ManyToManyField(
        Tags,
        verbose_name="Приём пищи",
        help_text="Укажите приём пищи (можно несколько)",
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время готовки",
        help_text="Укажите время приготовления рецепта в минутах",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("id",)

    def __str__(self):
        return self.name


class RecipesIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipes, related_name="recipe_ingredients", on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Игредиенты рецепта"
        verbose_name_plural = "Игредиенты рецептов"
        ordering = ("id",)


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, related_name="shoppingcart", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name="shoppingcart",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        ordering = ("id",)


class Favorite(models.Model):
    user = models.ForeignKey(
        User, related_name="favorite", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name="favorite",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        ordering = ("id",)
