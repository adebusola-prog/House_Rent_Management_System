from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
      path('login', views.LoginView.as_view(), name='login'),
      path('user/register', views.UserRegistrationView.as_view(), \
            name='user_register'),
      path('logout/', views.LogoutView.as_view(), name='logout'),
      path('change_password/<int:pk>', views.ChangePassword.as_view(),\
            name='change_password'),
      path('forgot_password/<int:pk>', views.ForgotPassword.as_view(),\
            name='forgot_password'),
      path('resetpassword/<int:uuidb64>/<token>', views.ResetPassword.as_view(), \
            name='reset_password'),
      path('password_reset_complete', views.SetNewPassword.as_view(), \
            name='password_reset_complete')
]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

