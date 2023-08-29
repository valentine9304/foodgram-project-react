from django.contrib import admin

from .models import (
    Tags,
    Ingredients,
    Recipes,
    RecipesIngredients,
    ShoppingCart,
    Favorite,
)


class AddIngredientsinRecipe(admin.TabularInline):
    """
    Возможность добавление ингридиентов в админ зоне Рецепта.
    """

    model = RecipesIngredients
    extra = 2


class TagsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "color")
    list_filter = ("name",)
    search_fields = ("name",)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "measurement_unit")
    list_filter = ("name",)
    search_fields = ("name",)


class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "name",
        "in_favorite",
    )
    inlines = [AddIngredientsinRecipe]

    def in_favorite(self, obj):
        return obj.favorite.all().count()


class RecipesIngredientsAdmin(admin.ModelAdmin):
    list_display = ("id", "recipe", "ingredient", "amount")
    list_filter = ("recipe", "ingredient")
    search_fields = ("recipe",)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recipe")
    list_filter = ("user",)
    search_fields = ("user",)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recipe")
    list_filter = ("user",)
    search_fields = ("user",)


admin.site.register(Tags, TagsAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(RecipesIngredients, RecipesIngredientsAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
