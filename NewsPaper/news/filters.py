import django_filters
from .models import Post, Author


class PostFilter(django_filters.FilterSet):
    posted = django_filters.DateFilter(lookup_expr='gt', label='Опубликовано после:')
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.ModelChoiceFilter(field_name='author', lookup_expr='exact', queryset=Author.objects.all())

    class Meta:
        model = Post
        fields = ['posted', 'title', 'author']
