from django_filters import rest_framework as filters

from yamdb.models import Title


class TitleFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year')
