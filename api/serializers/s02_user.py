from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from main import models

# Custom User Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser()
        exclude = (
            "password",
            "last_login",
            "date_joined",
            "groups",
            "user_permissions",
        )


# Login Serializer
class LoginSerializer(serializers.Serializer):
    email                   = serializers.CharField(required = False)
    phone                   = serializers.CharField(required = False)
    password                = serializers.CharField()
    device                  = serializers.CharField(required = False)
    token_type              = serializers.CharField()
    method                  = serializers.CharField()


# Check Reset Code Serializer
class ResetCodeSerializer(serializers.Serializer):
    check_type              = serializers.CharField()
    email                   = serializers.CharField(required = False)
    phone                   = serializers.CharField(required = False)
    code                    = serializers.CharField()
    password                = serializers.CharField(required = False)


# Register User Serializer
class RegisterUserSerializer(serializers.Serializer):
    reg_type                = serializers.CharField()
    email                   = serializers.CharField(required = False)
    phone                   = serializers.CharField(required = False)
    password                = serializers.CharField()


# Activate Account Serializer
class ActivateAccountSerializer(serializers.Serializer):
    act_type                = serializers.CharField()
    email                   = serializers.CharField(required = False)
    phone                   = serializers.CharField(required = False)
    code                    = serializers.CharField()


# Send Activation Code Serializer
class SendActivationCodeSerializer(serializers.Serializer):
    email                   = serializers.CharField(required = False)
    phone                   = serializers.CharField(required = False)
    act_type                = serializers.CharField()


# Change Email/Phone Number during Activation
class ChangeEmailPhoneSerializer(serializers.Serializer):
    change_type             = serializers.CharField()
    old_email               = serializers.CharField(required = False)
    old_phone               = serializers.CharField(required = False)
    email                   = serializers.CharField(required = False)
    phone                   = serializers.CharField(required = False)



# Send Reset Link Serializer
class SendResetLinkSerializer(serializers.Serializer):
    email                   = serializers.CharField(required = False)
    phone                   = serializers.CharField(required = False)
    method                  = serializers.CharField()


# Email Confirmation Token
class EmailConfirmationSerializer(serializers.Serializer):
    email                   = serializers.EmailField()


# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserNotification
        exclude = (
            "user",
        )






