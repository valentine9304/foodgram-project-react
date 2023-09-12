from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404

from recipes.models import (
    Tags,
    Ingredients,
    Recipes,
    RecipesIngredients,
    ShoppingCart,
    Favorite,
)
from users.models import Follow
from users.serializers import UserSerializer


class TagsSerializer(serializers.ModelSerializer):
    """Serializer для модели Tag."""

    class Meta:
        model = Tags
        fields = ("id", "name", "color", "slug")
        read_only_fields = ("__all__",)


class IngredientsSerializer(serializers.ModelSerializer):
    """Serializer для модели Ingredients."""

    class Meta:
        model = Ingredients
        fields = ("id", "name", "measurement_unit")
        read_only_fields = ("__all__",)


class RecipesIngredientsSerializer(serializers.ModelSerializer):
    """Serializer для модели RecipesIngredients."""

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipesIngredients
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class AddRecipesIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipesIngredients
        fields = ("id", "amount")


class RecipesSerializer(serializers.ModelSerializer):
    """Serializer для модели Recipes."""

    author = UserSerializer()
    tags = TagsSerializer(many=True)
    ingredients = RecipesIngredientsSerializer(
        many=True,
        source="recipe_ingredients",
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name="get_is_in_shopping_cart"
    )

    is_favorited = serializers.SerializerMethodField(
        method_name="get_is_favorited"
    )

    class Meta:
        model = Recipes
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "is_in_shopping_cart",
            "is_favorited",
            "cooking_time",
        )

    def get_is_in_shopping_cart(self, obj) -> bool:
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_is_favorited(self, obj) -> bool:
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()


class CreateRecipesSerializer(serializers.ModelSerializer):
    """Serializer для создания Recipes."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(), many=True
    )
    image = Base64ImageField()
    author = UserSerializer(default=serializers.CurrentUserDefault())
    ingredients = AddRecipesIngredientsSerializer(many=True)

    class Meta:
        model = Recipes
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            raise ValidationError("Нужно выбрать ингредиент.")
        ingredients_list = []
        for item in ingredients:
            ingredient = get_object_or_404(Ingredients, id=item["id"])
            if ingredient in ingredients_list:
                raise ValidationError("Ингридиенты повторяются.")
            if int(item["amount"]) <= 0:
                raise ValidationError({"Количество не может быть нулевым."})
            ingredients_list.append(ingredient)
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError("Нужно выбрать тег")
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError("Теги повторяются")
            tags_list.append(tag)
        return value

    def to_representation(self, instance):
        serializers = RecipesSerializer(instance)
        return serializers.data

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipes.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ingredient_data in ingredients_data:
            current_ingredient = Ingredients.objects.get(
                id=ingredient_data["id"]
            )
            amount = ingredient_data["amount"]
            RecipesIngredients.objects.create(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=amount,
            )
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        for ingredient_data in ingredients_data:
            current_ingredient = Ingredients.objects.get(
                id=ingredient_data["id"]
            )
            amount = ingredient_data["amount"]
            RecipesIngredients.objects.create(
                recipe=instance,
                ingredient=current_ingredient,
                amount=amount,
            )
        return instance


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Serializer для создания ShoppingCart."""

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.ReadOnlyField(read_only=True)
    image = serializers.ImageField(read_only=True)
    coocking_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ("id", "name", "image", "coocking_time")


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer для создания Избранного."""

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.ReadOnlyField(read_only=True)
    image = serializers.ImageField(read_only=True)
    coocking_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Favorite
        fields = ("id", "name", "image", "coocking_time")


class RecipeMiniSerializer(serializers.ModelSerializer):
    """Сериализатор для показа рецептов у тех на кого Подписан."""

    # image = Base64ImageField(read_only=True)
    # image = serializers.SerializerMethodField()
    # image = serializers.ImageField(source="recipes.image", read_only=True)
    # image = serializers.ImageField(read_only=True)

    class Meta:
        model = Recipes
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )

    # def get_image(self, recipe):
    #     request = self.context.get("request")
    #     # breakpoint()
    #     photo_url = recipe.image.url
    #     return request.build_absolute_uri(photo_url)
    #     # breakpoint()


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Подписчики.
    """

    email = serializers.ReadOnlyField(source="author.email")
    id = serializers.ReadOnlyField(source="author.id")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    # recipes = RecipeMiniSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj) -> bool:
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False

        return Follow.objects.filter(
            user=request.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        recipes = obj.author.recipes.all()
        if limit:
            recipes = recipes[: int(limit)]
        serializer = RecipeMiniSerializer(recipes, many=True, read_only=True)
        return serializer.data

    def get_recipes_count(self, obj) -> int:
        return obj.author.recipes.count()
