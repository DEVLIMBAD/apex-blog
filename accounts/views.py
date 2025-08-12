from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import(
    
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .forms import CustomUserCreationForm, CustomPasswordChangeForm, CustomSetPasswordForm, CustomUserCreationForm
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
import os

def user_logout(request):
    logout(request)
    return redirect('home')

print("TEMPLATES DIRS:", settings.TEMPLATES[0]['DIRS'])
print("LOOKING FOR:", os.path.join(settings.BASE_DIR, 'templates'))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    logout (request)
    return redirect('login')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'acoounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_engine = 'account/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

# class RegisterView(RegisterView):
#     template_name = 'registration/register.html'
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')


class RegisterView(CreateView):
    model = User
    form_class =CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

def user_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')

