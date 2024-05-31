from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, EmailSentView, EmailConfirmedView, EmailConfirmedFailedView, \
    ConfirmFromEmailView, UserNotFound, UserPasswordResetView

app_name = UsersConfig.name



urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('confirm_from_email/<str:uidb64>/<str:token>/', ConfirmFromEmailView.as_view(), name='confirm_from_email'),
    path('email_sent/', EmailSentView.as_view(), name='email_sent'),
    path('email_confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('email_confirmed_failed/', EmailConfirmedFailedView.as_view(), name='email_confirmed_failed'),
    path('not_found', UserNotFound.as_view(), name='not_found'),
    path('password_reset', UserPasswordResetView.as_view(), name='password_reset'),
]