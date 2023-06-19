from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from rest_framework import HTTP_HEADER_ENCODING, authentication
from .models import CustomUser
from house_rent_app.serializers import LocationSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
  
    class Meta:
        model = CustomUser
        fields = ("first_name", "middle_name", "last_name",  "email", "username", "referral_code",
                    "location", "phone_number","password", "confirm_password")
        
    def validate(self, attrs):
        """
        Validates the password and confirm_password fields.
        """
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs


class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer for user login.
    """

    @classmethod
    def get_token(cls, user):
        """
        Retrieves the token for the authenticated user and adds custom claims.
        """
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email

        return token


class ResetPasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for resetting user password.
    """

    class Meta:
        model = CustomUser
        fields = ('email',)
        extra_kwargs = {
            "email": {
                "write_only": True
            }
        }

    def validate_email(self, value):
        """
        Converts the email value to lowercase for consistency.
        """
        lower_email = value.lower()

        return lower_email


class SetNewPasswordSerializer(serializers.Serializer):
    """
    Serializer for setting a new user password.
    """

    token = serializers.CharField(min_length=1, write_only=True)  
    uuidb64 = serializers.CharField(min_length=1, write_only=True) 

    class Meta:
        model = CustomUser
        fields = ("password", "confirm_password", "token", "uuidb64") 

    def validate(self, attrs):
        """
        Validates the password and confirm_password fields and sets the new password for the user.
        """
        try:
            if attrs.get('password') != attrs.get('confirm_password'):
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match."})
            token = attrs.get('token')
            uuidb64 = attrs.get('uuidb64')

            id = force_str(urlsafe_base64_decode(uuidb64))
            account = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(account, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            account.set_password(attrs.get('password'))
            account.save()
        
        except Exception:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password', 'confirm_password')

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data.get('new_password'))
        instance.save()

        return instance


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("first_name", "email", "middle_name", "last_name", "username", 
                    "profile_picture", "phone_number", "customer_location")


