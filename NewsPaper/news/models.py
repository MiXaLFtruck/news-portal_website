from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from news.resources.constants import OPTIONS, article

# Create your models here.


class Author(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))

    def update_rating(self):
        updated = 0
        posts = Post.objects.filter(author=self)  # все посты автора
        author_cmnts = Comments.objects.filter(author=self.user_id)  # все комментарии автора

        for p in posts:
            updated += p.rating * 3  # суммарный рейтинг каждой статьи автора умножается на 3

            post_cmnts = Comments.objects.filter(post=p)  # все комментарии под постом p
            for pc in post_cmnts:
                updated += pc.rating  # суммарный рейтинг всех комментариев к статьям автора

        for ac in author_cmnts:
            updated += ac.rating  # суммарный рейтинг всех комментариев автора

        self.rating = updated
        self.save()

    def __str__(self):
        return self.user_id.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Category's name"))
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
    subscribers = models.ManyToManyField(User, null=True, verbose_name=_('Subscribers'))

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('Author'))
    article_or_news = models.CharField(max_length=2, choices=OPTIONS, default=article, verbose_name=_('Article/News'))
    posted = models.DateTimeField(auto_now_add=True, verbose_name=_('Posted on'))
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name=_('Category'))
    title = models.CharField(max_length=128, verbose_name=_('Title'))
    text = models.TextField(verbose_name=_('Text'))
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{str(self.text)[:123]}...'

    def __str__(self):
        return self.title[:30]

    def get_absolute_url(self):
        return reverse_lazy('post_details', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f"post-{self.pk}")


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.text[:30]
