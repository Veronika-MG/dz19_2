from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, FormView

from users.forms import UserRegisterForm, UserProfileForm, ResetForm
from users.models import User


class RegisterView(CreateView):
    """ Класс для регистрации пользователя."""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """ Переопределение метода для верификации почты."""
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse('users:confirm_from_email', kwargs={'uidb64': uid, 'token': token})

        send_mail(
            'Подтвердите адрес электронной почты',
            f'Для окончания регистрации необходимо подтвердить вашу электронную почту.\
            Чтобы это сделать, перейдите по ссылке: http://localhost:8000{activation_url}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

        return redirect('users:email_sent')

class EmailSentView(TemplateView):
    """ Класс для отображения отправки письма. """
    template_name = 'users/email_sent.html'

class ConfirmFromEmailView(View):
    """ Класс для обработки ссылки подтверждения. """
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        return redirect('users:email_confirmed_failed')

class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'

class EmailConfirmedFailedView(TemplateView):
    template_name = 'users/email_confirmed_failed.html'

class UserPasswordResetView(FormView):
    """ Класс восстановление пароля. """
    template_name = 'users/password_reset_form.html'
    form_class = ResetForm


    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None:
            new_password = User.objects.make_random_password(length=8)
            user.set_password(new_password)
            user.save()
            send_mail(
            'Ваш новый пароль.',
            f'Для входа используйте новый пароль: {new_password}.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
            return redirect('users:email_sent')
        return redirect('users:not_found')

class UserNotFound(TemplateView):
    template_name = 'users/not_found.html'

class ProfileView(UpdateView):
    """ Класс редактирования профиля пользователя. """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
