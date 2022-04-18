from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import ProfileForm, LoginForm, RegisterForm
from django.contrib.auth.models import User, Group
from news.views import News

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView

from django.shortcuts import redirect
from django.contrib import messages


class EditProfile(LoginRequiredMixin, UpdateView, News):
    template_name = 'edit-user.html'
    form_class = ProfileForm
    success_url = reverse_lazy('edit_profile')

    def get_object(self, **kwargs):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return context


class LoginFormView(SuccessMessageMixin, LoginView):
    success_message = "Вы успешно вошли в систему"
    template_name = 'login.html'
    form_class = LoginForm


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = '/accounts/login/'
    template_name = 'register.html'

    def get_success_url(self):
        messages.success(self.request, 'Вы успешно зарегистрировались. Воспользуйтесь логином и паролем, чтобы войти '
                                       'в систему')
        return self.success_url


@login_required
def to_authors(request):
    user = request.user
    group = Group.objects.get(name='Authors')
    if not user.groups.filter(name='Authors').exists():
        group.user_set.add(user)
        messages.success(request, 'Вы успешно добавлены в группу "Авторы"')
    else:
        messages.warning(request, 'Вы уже состоите в группе "Авторы"')

    return redirect('edit_profile')
