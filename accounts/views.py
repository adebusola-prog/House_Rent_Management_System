from django.shortcuts import render
from .serializers import LoginSerializer, ChangePasswordSerializer, \
    UserRegistrationSerializer, ResetPasswordSerializer, SetNewPasswordSerializer
from .models import CustomUser, HouseOwner, Tenant
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from .utils import Utils


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
   

class ChangePasswordAV(generics.UpdateAPIView):
    queryset = CustomUser.active_objects.all()
    serializer_class = ChangePasswordSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        print(serializer.is_valid())
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            first_name = serializer.validated_data.get("first_name")
            last_name = serializer.validated_data.get("last_name")
            email = serializer.validated_data.get("email")
            signuptype = serializer.validated_data.get("signuptype")
            print(email)
            print(serializer.data)
            password = serializer.validated_data.get("password")
            # confirm_password = serializer.validated_data.get("password2")
            account = CustomUser.objects.create_user(
                first_name=first_name, last_name=last_name, username=username,
                email = email, password=password, signuptype=signuptype)
            if account.signuptype == 'H.O':
                HouseOwner.objects.get_or_create(user=account)
            else:
                Tenant.objects.get_or_create(user=account)
            data["status"] = "success"
            data["username"] = account.username
            data["email"] = account.email
            refresh_token = RefreshToken.for_user(account)
            data["refresh_token"] = str(refresh_token)
            data["access_token"] = str(refresh_token.access_token)
            return Response(data, status=status.HTTP_201_CREATED)
        data["error"] = serializer.errors
        data["status"] = "error"
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    

class ForgotPasswordAV(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        lower_email = serializer.validated_data.get("email").lower()
        if CustomUser.objects.filter(email__iexact=lower_email).exists():
            account = CustomUser.objects.get(email=lower_email)
            uuidb64 = urlsafe_base64_encode(account.id)
            token = PasswordResetTokenGenerator().make_token(account)
            current_site = get_current_site(
                request).domain
            relative_path = reverse(
                "reset-password", kwargs={"uuidb64": uuidb64, "token": token})
            abs_url = "http://" + current_site + relative_path

            mail_subject = "Please Reset your CustomUser Password"
            message = "Hi" + account.username + "," + \
                " Please Use the Link below to reset your account passwors:" + "" + abs_url

            Utils.send_email(mail_subject, message, account.email)
        return Response({"status": "success", "message": "We have sent a password-reset link to the email you provided.Please check and reset  "}, status=status.HTTP_200_OK)


class ResetPasswordAV(APIView):
    serializer_class = ResetPasswordSerializer
  
    def get(self, request, uuidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uuidb64))
            account = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(account, token):
                return Response({"status": "fail", "message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": "success", "message": "Your credentials valid", "uuidb64": uuidb64, "token": token}, status=status.HTTP_400_BAD_REQUEST)
        except DjangoUnicodeDecodeError as e:
            return Response({"status": "fail", "message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAV(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
   
