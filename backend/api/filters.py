import django_filters
from django_filters import rest_framework
from rest_framework import filters

from recipes.models import Recipe
from users.models import UserProfile


class RecipeFilter(django_filters.FilterSet):
    is_favorited = rest_framework.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='filter_is_in_shopping_cart',
    )
    tags = rest_framework.AllValuesMultipleFilter(field_name='tags__slug')
    author = django_filters.ModelChoiceFilter(
        queryset=UserProfile.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')

    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return queryset
        if not value:
            return queryset.exclude(favorites__user=self.request.user)
        return queryset.filter(favorites__user=self.request.user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return queryset
        if not value:
            return queryset.exclude(shopping_cart__user=self.request.user)
        return queryset.filter(shopping_cart__user=self.request.user)


class IngredientFilter(filters.SearchFilter):
    search_param = 'name'
