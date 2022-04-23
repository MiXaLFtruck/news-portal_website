from django.contrib import admin
from .models import Category, Post, Author, Comments
from modeltranslation.admin import TranslationAdmin

# Register your models here.


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


class CommentsAdmin(TranslationAdmin):
    model = Comments


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comments)
