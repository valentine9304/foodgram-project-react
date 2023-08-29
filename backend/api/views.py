from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from .serializers import (
    TagsSerializer,
    IngredientsSerializer,
    RecipesSerializer,
    CreateRecipesSerializer,
    ShoppingCartSerializer,
    FavoriteSerializer,
)
from recipes.models import Tags, Ingredients, Recipes, ShoppingCart, Favorite
from .pagination import RecipesPagination
from .filter import RecipeFilter, IngredientsFilter
from .permissions import IsAuthorOrAdminOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Функция для модели тегов."""

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (AllowAny,)


class IngredientsViewSet(viewsets.ModelViewSet):
    """Функция для модели ингридиентов."""

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientsFilter
    permission_classes = (AllowAny,)


class RecipesViewSet(viewsets.ModelViewSet):
    """Функция для модели ингридиентов."""

    queryset = Recipes.objects.all().order_by("-id")
    serializer_class = RecipesSerializer
    pagination_class = RecipesPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    # permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipesSerializer
        return CreateRecipesSerializer

    @action(
        detail=True,
        methods=["post", "delete"],
        # permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        """
        Список покупок. Добавление, удаления рецепта у пользователя.
        """
        recipe = get_object_or_404(Recipes, id=pk)
        user = self.request.user

        if request.method == "POST":
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    "Рецепт уже в списке покупок.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = ShoppingCartSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        if not ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                "Рецепта нет в списке покупок.",
                status=status.HTTP_404_NOT_FOUND,
            )
        ShoppingCart.objects.get(user=user, recipe=recipe).delete()
        return Response(
            "Рецепт удалён из списка покупок.",
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        detail=True,
        methods=["post", "delete"],
        # permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        """
        Список избранного.
        Добавление, удаления рецепта в Избранное пользователя.
        """
        recipe = get_object_or_404(Recipes, id=pk)
        user = self.request.user

        if request.method == "POST":
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    "Рецепт уже в Избранном.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = FavoriteSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        if not Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                "Рецепта нет в Избранном.",
                status=status.HTTP_404_NOT_FOUND,
            )
        Favorite.objects.get(user=user, recipe=recipe).delete()
        return Response(
            "Рецепт удалён из Избранного",
            status=status.HTTP_204_NO_CONTENT,
        )
