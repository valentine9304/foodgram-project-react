from django_filters.rest_framework import FilterSet, filters

from recipes.models import Recipes, Tags, Ingredients
from users.models import User


class RecipeFilter(FilterSet):
    is_favorited = filters.BooleanFilter(method="get_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="get_is_in_shopping_cart"
    )
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tags.objects.all(),
    )

    def get_is_in_shopping_cart(self, queryset, name, value):
        # breakpoint()
        if self.request.user.is_authenticated and value:
            return queryset.filter(shoppingcart__user=self.request.user)
        return queryset

    def get_is_favorited(self, queryset, name, value):
        # breakpoint()
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    class Meta:
        model = Recipes
        fields = ("tags", "author")


class IngredientsFilter(FilterSet):
    name = filters.CharFilter(lookup_expr="istartswith")

    class Meta:
        model = Ingredients
        fields = ("name",)
