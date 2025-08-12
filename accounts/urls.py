from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import user_logout, RegisterView

from django.urls import reverse_lazy

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/register/', auth_views.RegisterView.as_view(), name='register'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.user_logout, name='logout'),
    # path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    #path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
   # path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='passwor_reset_confirm'),
   # path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('accounts/password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='account/password_reset.html',
            email_template_name='account/password_reset_email.html',
            subject_template_name='account/password_reset_subject.txt',
            success_url=reverse_lazy('password_reset_done')
            
        ),
        name='password_reset'),

    path('accounts/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='account/password_reset_done.html'  # Changed from registration/
        ),
        name='password_reset_done'),




   path('accounts/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete')
        ),
        name='password_reset_confirm'),
    
    path('accounts/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'),

]
