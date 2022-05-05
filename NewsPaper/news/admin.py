from django.contrib import admin
from .models import Category, Post, Author, Comments
from modeltranslation.admin import TranslationAdmin

# Register your models here.


class CategoryTranslationAdmin(TranslationAdmin):
    model = Category


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'posted', 'rating']
    search_fields = ['title', ]


class PostTranslationAdmin(TranslationAdmin):
    model = Post


class CommentsTranslationAdmin(TranslationAdmin):
    model = Comments


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Comments)
