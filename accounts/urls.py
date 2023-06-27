from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
      path('login', views.LoginView.as_view(), name='login'),
      path('user/register', views.UserRegistrationView.as_view(), \
            name='user_register'),
      path('logout/', views.LogoutView.as_view(), name='logout'),
      path('change_password/<int:pk>', views.ChangePasswordAV.as_view(),\
            name='change_password'),
      path('forgot_password/<int:pk>', views.ForgotPasswordAV.as_view(),\
            name='forgot_password'),
      path('resetpassword/<int:uuidb64>/<token>', views.ResetPasswordAV.as_view(), \
            name='reset_password'),
      path('password_reset_complete', views.SetNewPasswordAV.as_view(), \
            name='password_reset_complete')
]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

