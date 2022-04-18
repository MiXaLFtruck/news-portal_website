from django.urls import path
from .views import EditProfile, LoginFormView, RegisterView, to_authors
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('profile/', EditProfile.as_view(), name='edit_profile'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('add-me-to-authors/', to_authors, name='add-me-to-authors'),
]
