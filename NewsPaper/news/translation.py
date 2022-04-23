from .models import Category, Post, Comments
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOption(TranslationOptions):
    fields = ('name', )


@register(Post)
class PostTranslationOption(TranslationOptions):
    fields = ('title', 'text', )


@register(Comments)
class CommentsTranslationOption(TranslationOptions):
    fields = ('text', )

