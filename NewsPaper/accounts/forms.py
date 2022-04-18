from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


class ProfileForm(forms.ModelForm):
    username = forms.CharField(required=True, label='Имя пользователя (login)', help_text='', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_joined': forms.DateTimeInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
    )


class RegisterForm(UserCreationForm):
    username = forms.CharField(required=True, label='Имя пользователя (обязательно)', help_text='',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label='E-mail (обязательно)', widget=forms.EmailInput(attrs={'class':
                                                                                                   'form-control'}))
    first_name = forms.CharField(required=False, label="Имя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, label="Фамилия", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save()
        common_group = Group.objects.get(name='Common')
        common_group.user_set.add(user)
        return user
