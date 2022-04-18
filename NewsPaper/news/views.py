from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin, View
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Post, Category
from .forms import PostForm
from .filters import PostFilter

from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import redirect
from django.contrib import messages

from django.core.cache import cache


class News(ContextMixin, View):
    paginate_by = 3

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        return {
            **super().get_context_data(**kwargs),
            'categories': categories,
        }


class NewsList(News, ListView):
    model = Post
    template_name = 'news-list.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-posted')

    def get_context_data(self, **kwargs):
        posts_total = self.queryset.count()
        return {
            **super().get_context_data(**kwargs),
            'posts_total': posts_total,
        }


class NewsDetails(News, DetailView):
    model = Post
    template_name = 'post-details.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f"post-{self.kwargs['pk']}", None)

        if not obj:
            obj = super().get_object(*args, **kwargs)
            cache.set(f"post-{self.kwargs['pk']}", obj)

        return obj


class InCategoryList(News, ListView):
    model = Post
    template_name = 'news-list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(postcategory__category__name=self.kwargs['name']).order_by('-posted')

    def get_context_data(self, **kwargs):
        posts_total = self.get_queryset().count()
        user = self.request.user
        category = Category.objects.get(name=self.kwargs['name'])
        category_subscribers = User.objects.filter(category=category)
        user_is_subscribed = user in category_subscribers
        return {
            **super().get_context_data(**kwargs),
            'posts_total': posts_total,
            'category': self.kwargs['name'],
            'user_is_subscribed': user_is_subscribed
        }


class SearchNews(News, ListView):
    model = Post
    # queryset = Post.objects.order_by('-posted')
    template_name = 'search-news.html'
    context_object_name = 'search_news'

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs.order_by('-posted')

    def get_context_data(self, *args, **kwargs):
        posts_total = self.get_queryset().count()
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
            'posts_total': posts_total
        }


class AddNews(PermissionRequiredMixin, News, CreateView):
    permission_required = ('news.add_post', )
    template_name = 'add-news.html'
    form_class = PostForm

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         html_content = render_to_string('new-post-in-category.html', {'title': request.POST['title'],
    #                                                                       'text': request.POST['text'], 'username':
    #                                                                           request.user.username})
    #         categories = request.POST.getlist('category')
    #         recipients = []
    #         for id in categories:
    #             for user in Category.objects.get(pk=int(id)).subscribers.all():
    #                 email = user.email
    #                 if email and email not in recipients:
    #                     recipients.append(email)
    #
    #         msg = EmailMultiAlternatives(
    #             subject=f'{request.POST["title"]}',
    #             body="",
    #             from_email='sbsochi@yandex.ru',
    #             to=recipients
    #         )
    #         msg.attach_alternative(html_content, "text/html")
    #         msg.send()
    #
    #     return super(AddNews, self).post(request, *args, **kwargs)


class EditNews(PermissionRequiredMixin, News, UpdateView):
    permission_required = ('news.change_post', )
    template_name = 'add-news.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class DeleteNews(News, DeleteView):
    template_name = 'delete-news.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news_list')


# функция подписки на категорию новостей. вешается на кнопку
def subscribe_for_category(request, name):
    current_user = request.user
    category = Category.objects.get(name=name)
    if current_user.is_authenticated:
        category.subscribers.add(current_user)
        messages.success(request, f'Вы успешно подписались на новости в категории {category.name}')
        return redirect('incategory_list', name)
    else:
        messages.error(request, 'Для выполнения данного действия необходимо авторизоваться в системе')
        return redirect('login')
