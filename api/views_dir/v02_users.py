
from rest_framework.views import APIView, Response
from django.core.mail import send_mail, EmailMessage
from django.utils.html import strip_tags
from django.utils import crypto
from django.conf import settings
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from phonenumber_field import phonenumber
import datetime

from api.serializers import s02_user
from main.models_dir import m02_users



name = "Real Estate"

class UsersApi(APIView):
    def post(self, request):
        data = request.data.get('action')

        if data == 'login':
            return self.login(request)
        
        if data == 'logout':
            return self.logout(request)
        
        if data == 'send_reset_link':
            return self.send_reset_link(request)
        
        if data == 'send_reset_link':
            return self.send_reset_link(request)
        
        if data == 'check_reset_code':
            return self.check_reset_code(request)
        
        if data == 'activate_code':
            return self.activate_code(request)
        
        if data == 'send_activate_code':
            return self.send_activate_code(request)
        
        if data == 'change_email_phone':
            return self.change_email_phone(request)
        
        if data == 'email_confirmation':
            return self.login(request)

        if data == 'check_tokens':
            return self.check_tokens(request)

        if data == 'register_user':
            return self.register_user(request)

        if data == 'get_notifications':
            return self.get_notifications(request)
    
    # Login Functionality
    def login(self, request):
        serializer = s02_user.LoginSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'code': 'not_valid',
            })

        data = serializer.validated_data

        email           = data.get("email")
        phone           = data.get("phone")
        token_type      = data.get('token_type')
        device          = data.get("device")
        password        = data.get("password")
        method          = data.get("method")
        
        if method == "email":
            user = m02_users.CustomUser.objects.filter(email = email)
            if user.count() == 0:
                return Response({
                    "status": "error",
                    "code": "user_not_valid",
                })
            
            user = user.first()
            user_serializer = s02_user.CustomUserSerializer(user)

            
            if not user.check_password(password):
                return Response({
                    "status": "error",
                    "code": "pass_not_valid",
                })

            auth_tokens = m02_users.AuthTokens.objects.filter(
                user = user,
                token_type = token_type,
            )

            for auth_token in auth_tokens:
                auth_token.delete()

            
            tokens = crypto.get_random_string(512)
            
            auth_token              = m02_users.AuthTokens()
            auth_token.user         = user
            auth_token.tokens       = tokens
            auth_token.token_type   = token_type
            auth_token.device       = device
            auth_token.save()

            

            return Response({
                "status": "ok",
                "phone_confirmation": user.phone_confirmed,
                "email_confirmation": user.email_confirmed,
                "token": tokens,
                "data": user_serializer.data,
            })

            
        if method == "phone":
            user = m02_users.CustomUser.objects.filter(phone = phone)
            if user.count() == 0:
                return Response({
                    "status": "error",
                    "code": "user_not_valid",
                })
            
            user = user.first()
            user_serializer = s02_user.CustomUserSerializer(user)

            if not user.check_password(password):
                return Response({
                    "status": "error",
                    "code": "pass_not_valid",
                })
            
            
            auth_tokens = m02_users.AuthTokens.objects.filter(
                user = user,
                token_type = token_type,
                device = device,
            )

            for auth_token in auth_tokens:
                auth_token.delete()

            
            tokens = crypto.get_random_string(512)
            
            auth_token              = m02_users.AuthTokens()
            auth_token.user         = user
            auth_token.tokens       = tokens
            auth_token.token_type   = token_type
            auth_token.device       = device
            auth_token.save()

            return Response({
                "status": "ok",
                "phone_confirmation": user.phone_confirmed,
                "email_confirmation": user.email_confirmed,
                "token": tokens,
                "data": user_serializer.data,
            })
        
        return Response({
            "status": "error",
            "code": "method_not_valid",
        })
    
    # Send Reset Link
    def send_reset_link(self, request):
        serializer = s02_user.SendResetLinkSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'code': 'not_valid',
            })

        data = serializer.validated_data
        email           = data.get("email")
        phone           = data.get("phone")
        method          = data.get("method")
        
        if method == "email":
            
            if m02_users.CustomUser.objects.filter(email = email).count() == 0:
                return Response({
                    "status": "error",
                    "code": "email_not_found",
                })
            
            user                        = m02_users.CustomUser.objects.get(email = email)

            if m02_users.EmailPhoneConfirmation.objects.filter(
                user = user,
                method = method,
                exp_date__gt = datetime.date.today(),
            ).count() > 0:
                code_model = m02_users.EmailPhoneConfirmation.objects.get(
                    user = user,
                    method = method,
                    exp_date__gt = datetime.date.today(),
                )
                code_model.email_count += 1
                code_model.save()

                if code_model.email_count > 5:
                    return Response({
                        "status": "error",
                        "code": "email_reached",
                    })


            else:
                code                        = crypto.get_random_string(6, "0123456789")
                code_model                  = m02_users.EmailPhoneConfirmation()
                code_model.user             = user
                code_model.method           = method
                code_model.exp_date         = datetime.timedelta(hours=32) + datetime.date.today()
                code_model.tokens           = code
                code_model.email_count      = 1
                code_model.save()
        

            message = render_to_string("accounts/reset_code.html", {
                "name": name,
                "customuser": user,
                "code": code_model.tokens,
            })

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [f"{user.email}", ]

            email_msg = EmailMessage(
                subject = f"{name}: Password Reset Code",
                body = message,
                from_email = email_from,
                to = recipient_list,
            )

            try:
                email_msg.content_subtype = "html"
                email_msg.send()
            except: pass

            return Response({
                "status": "ok",
            })

            
        if method == "phone":
            if m02_users.CustomUser.objects.filter(phone = phone).count() == 0:
                return Response({
                    "status": "error",
                    "code": "phone_not_found",
                })
            
            user                        = m02_users.CustomUser.objects.get(phone = phone)
            
            if m02_users.EmailPhoneConfirmation.objects.filter(
                user = user,
                method = method,
                exp_date__gt = datetime.date.today(),
            ).count() > 0:
                code_model = m02_users.EmailPhoneConfirmation.objects.get(
                    user = user,
                    method = method,
                    exp_date__gt = datetime.date.today(),
                )

                code_model.sms_count += 1
                code_model.save()

                if code_model.sms_count > 3:
                    return Response({
                        "status": "error",
                        "code": "sms_reached",
                    })
                
            else:

                code                        = crypto.get_random_string(6, "0123456789")
                code_model                  = m02_users.EmailPhoneConfirmation()
                code_model.user             = user
                code_model.method           = method
                code_model.exp_date         = datetime.timedelta(hours=32) + datetime.date.today()
                code_model.tokens           = code
                code_model.sms_count        = 1
                code_model.save()
    
            message = f"Password reset code is: {code_model.tokens}\nRemember This code is valid for 24 hours."

            # Some kind of code to call sms sending api

            return Response({
                "status": "ok",
            })
        
    # Check Reset Code or Change Password with reset code
    def check_reset_code(self, request):
        serializer = s02_user.ResetCodeSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'code': 'not_valid',
            })

        data            = serializer.validated_data
        check_type      = data.get("check_type")
        email           = data.get("email")
        phone           = data.get("phone")
        code            = data.get("code")
        password        = data.get("password")

        if email:
            code_model = m02_users.EmailPhoneConfirmation.objects.filter(
                user__email = email,
                tokens      = code
            )

            if code_model.count() == 0:
                return Response({
                    "status": "error",
                    "code": "invalid_code"
                })
        
        if phone:
            code_model = m02_users.EmailPhoneConfirmation.objects.filter(
                user__phone = phone,
                tokens      = code
            )

            if code_model.count() == 0:
                return Response({
                    "status": "error",
                    "code": "invalid_code"
                })

        if check_type == "check":
            return Response({
                "status": "ok",
                "code": "code_valid"
            })
        

        if check_type == "reset":
            user = code_model.first().user
            user.set_password(password)
            user.save()
            code_model.first().delete()

            message = render_to_string("accounts/password_changed.html", {
                "name": name,
                "customuser": user,
                "date": datetime.date.today(),
            })

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [f"{user.email}", ]

            email_msg = EmailMessage(
                subject = f"{name}: Password Changed",
                body = message,
                from_email = email_from,
                to = recipient_list,
            )

            try:
                email_msg.content_subtype = "html"
                email_msg.send()
            except: pass

            return Response({
                "status": "ok",
                "code": "pass_reset",
            })
        
        return Response({
            "status": "error",
            "code": "not_valid",
        })

    # Register User
    def register_user(self, request):
        serializer = s02_user.RegisterUserSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'code': 'not_valid',
            })

        data            = serializer.validated_data
        reg_type        = data.get("reg_type")
        phone           = data.get("phone")
        email           = data.get("email")
        password        = data.get("password")

        if reg_type == "email":
            if m02_users.CustomUser.objects.filter(email = email).count() > 0:
                return Response({
                    "status": "error",
                    "code": "email_exists",
                })
            
            
            user            = m02_users.CustomUser()
            user.email      = email
            
            user.set_password(password)
            
            user.save()

            code                        = crypto.get_random_string(6, "0123456789")
            code_model                  = m02_users.EmailPhoneConfirmation()
            code_model.user             = user
            code_model.method           = "email"
            code_model.exp_date         = datetime.timedelta(days=3) + datetime.date.today()
            code_model.tokens           = code
            code_model.email_count      = 1
            code_model.save()
            
            host_address = f"{settings.CORS_ALLOWED_ORIGINS[0]}/activation/{code}"

            subject = f'{ name }: Account Activation'
            message = render_to_string("accounts/activation_code.html", {
                "name": name,
                "customuser": user,
                "code": code,
                "link": host_address,
                "hour": 72,
            })

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [f"{user.email}", ]

            email_msg = EmailMessage(
                subject = subject,
                body = message,
                from_email = email_from,
                to = recipient_list,
            )

            email_msg.content_subtype = "html"

            try:
                email_msg.send()
            except: pass

            return Response({
                "status": "ok",
            })

        if reg_type == "phone":
            if m02_users.CustomUser.objects.filter(phone = phone).count() > 0:
                return Response({
                    "status": "error",
                    "code": "phone_exists",
                })

            user            = m02_users.CustomUser()
            user.phone      = phone
            
            user.set_password(password)
            
            user.save()

            code                        = crypto.get_random_string(6, "0123456789")
            code_model                  = m02_users.EmailPhoneConfirmation()
            code_model.user             = user
            code_model.method           = "phone"
            code_model.exp_date         = datetime.timedelta(days=3) + datetime.date.today()
            code_model.tokens           = code
            code_model.email_count      = 1
            code_model.save()
            
            message = f"Phone number activation code is: {code_model.tokens}\nRemember This code is valid for 72 hours."

            # Some kind of code to call sms sending api

            return Response({
                "status": "ok",
            })

        return Response({
            "status": "ok",
        })
    
    # Logout Functionality
    def logout(self, request):
        tokens = request.data.get("tokens")
        token_model = m02_users.AuthTokens.objects.filter(tokens=tokens)
        if token_model.count() == 0:
            return Response({
                "status": "error",
                "code": "token_expired",
            })
        
        token_model.first().delete()

        return Response({
            "status": "ok",
        })

    # Check Tokens
    def check_tokens(self, request):
        tokens = request.data.get("tokens")
        token_model = m02_users.AuthTokens.objects.filter(tokens=tokens)
        if token_model.count() == 0:
            return Response({
                "status": "error",
                "code": "token_expired",
            })
        
        user = token_model.first().user
        user_serializer = s02_user.CustomUserSerializer(user)

        return Response({
            "status": "ok",
            "data": user_serializer.data,
        })

    # Activate Code
    def activate_code(self, request):
        serializer = s02_user.ActivateAccountSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'code': 'not_valid',
            })
        
        data                    = serializer.validated_data
        act_type                = data.get("act_type")
        email                   = data.get("email")
        phone                   = data.get("phone")
        code                    = data.get("code")

        if act_type == "email":
            if m02_users.EmailPhoneConfirmation.objects.filter(
                user__email = email,
                tokens      = code,
                method      = act_type,
                exp_date__gt= datetime.date.today()

            ).count() == 0:
                return Response({
                    "status": "error",
                    "code": "invalid_code",
                })
            
            code_model  = m02_users.EmailPhoneConfirmation.objects.filter(
                user__email = email,
                tokens      = code,
                method      = act_type,
                exp_date__gt= datetime.date.today()
            ).first()

            user                    = code_model.user
            user.email_confirmed    = True
            user.save()

            code_model.delete()

            return Response({
                "status": "ok",
            })
        
        if act_type == "phone":
            if m02_users.EmailPhoneConfirmation.objects.filter(
                user__phone = phone,
                tokens      = code,
                method      = act_type,
                exp_date__gt= datetime.date.today()

            ).count() == 0:
                return Response({
                    "status": "error",
                    "code": "invalid_code",
                })
            
            code_model  = m02_users.EmailPhoneConfirmation.objects.filter(
                user__phone = phone,
                tokens      = code,
                method      = act_type,
                exp_date__gt= datetime.date.today()
            ).first()

            user                    = code_model.user
            user.phone_confirmed    = True
            user.save()

            code_model.delete()

            return Response({
                "status": "ok",
            })
        
        return Response({
            "status": "ok",
        })

    # Send Activate Code
    def send_activate_code(self, request):
        serializer = s02_user.SendActivationCodeSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'code': 'not_valid',
            })
        
        data                    = serializer.validated_data
        act_type                = data.get("act_type")
        email                   = data.get("email")
        phone                   = data.get("phone")

        if act_type == "email":
            
            if m02_users.CustomUser.objects.filter(email = email).count() == 0:
                return Response({
                    "status": "error",
                    "code": "email_not_found",
                })
            
            user                        = m02_users.CustomUser.objects.get(email = email)

            if m02_users.EmailPhoneConfirmation.objects.filter(
                user = user,
                method = act_type,
                exp_date__gt = datetime.date.today(),
            ).count() > 0:
                code_model = m02_users.EmailPhoneConfirmation.objects.get(
                    user = user,
                    method = act_type,
                    exp_date__gt = datetime.date.today(),
                )
                code_model.email_count += 1
                code_model.save()

                code = code_model.tokens

                if code_model.email_count > 5:
                    return Response({
                        "status": "error",
                        "code": "email_reached",
                    })


            else:
                code                        = crypto.get_random_string(6, "0123456789")
                code_model                  = m02_users.EmailPhoneConfirmation()
                code_model.user             = user
                code_model.method           = act_type
                code_model.exp_date         = datetime.timedelta(hours=32) + datetime.date.today()
                code_model.tokens           = code
                code_model.email_count      = 1
                code_model.save()

            host_address = f"{settings.CORS_ALLOWED_ORIGINS[0]}/activation/{code}"

            message = render_to_string("accounts/activation_code.html", {
                "name": name,
                "customuser": user,
                "code": code_model.tokens,
                "link": host_address,
                "hour": 32,
            })

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [f"{user.email}", ]

            email_msg = EmailMessage(
                subject = f"{name}: Email Activation",
                body = message,
                from_email = email_from,
                to = recipient_list,
            )

            try:
                email_msg.content_subtype = "html"
                email_msg.send()
            except: pass

            return Response({
                "status": "ok",
            })

            
        if act_type == "phone":
            if m02_users.CustomUser.objects.filter(phone = phone).count() == 0:
                return Response({
                    "status": "error",
                    "code": "phone_not_found",
                })
            
            user                        = m02_users.CustomUser.objects.get(phone = phone)
            
            if m02_users.EmailPhoneConfirmation.objects.filter(
                user = user,
                method = act_type,
                exp_date__gt = datetime.date.today(),
            ).count() > 0:
                code_model = m02_users.EmailPhoneConfirmation.objects.get(
                    user = user,
                    method = act_type,
                    exp_date__gt = datetime.date.today(),
                )

                code_model.sms_count += 1
                code_model.save()

                if code_model.sms_count > 3:
                    return Response({
                        "status": "error",
                        "code": "sms_reached",
                    })
                
            else:

                code                        = crypto.get_random_string(6, "0123456789")
                code_model                  = m02_users.EmailPhoneConfirmation()
                code_model.user             = user
                code_model.method           = act_type
                code_model.exp_date         = datetime.timedelta(hours=32) + datetime.date.today()
                code_model.tokens           = code
                code_model.sms_count        = 1
                code_model.save()
    
            message = f"Phone number activation code is: {code_model.tokens}\nRemember This code is valid for 24 hours."

            # Some kind of code to call sms sending api

            return Response({
                "status": "ok",
            })
        
        return Response({
            "status": "ok",
        })

    # Change Email/Phone Number
    def change_email_phone(self, request):
        serializer = s02_user.ChangeEmailPhoneSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'code': 'not_valid',
            })
        
        data                    = serializer.validated_data
        change_type             = data.get("change_type")
        old_email               = data.get("old_email")
        old_phone               = data.get("old_phone")
        email                   = data.get("email")
        phone                   = data.get("phone")

        if change_type == "email":
            if m02_users.CustomUser.objects.filter(email = old_email).count() == 0:
                return Response({
                    "status": "error",
                    "code": "email_not_found",
                })
            
            user                        = m02_users.CustomUser.objects.get(email = old_email)
            user.email                  = email
            user.save()

            if m02_users.EmailPhoneConfirmation.objects.filter(
                user = user,
                method = change_type,
                exp_date__gt = datetime.date.today(),
            ).count() > 0:
                code_model = m02_users.EmailPhoneConfirmation.objects.get(
                    user = user,
                    method = change_type,
                    exp_date__gt = datetime.date.today(),
                )
                code_model.email_count += 1
                code_model.save()

                if code_model.email_count > 5:
                    return Response({
                        "status": "error",
                        "code": "email_reached",
                    })


            else:
                code                        = crypto.get_random_string(6, "0123456789")
                code_model                  = m02_users.EmailPhoneConfirmation()
                code_model.user             = user
                code_model.method           = change_type
                code_model.exp_date         = datetime.timedelta(hours=32) + datetime.date.today()
                code_model.tokens           = code
                code_model.email_count      = 1
                code_model.save()

            host_address = f"{settings.CORS_ALLOWED_ORIGINS[0]}/activation/{code}"

            message = render_to_string("accounts/activation_code.html", {
                "name": name,
                "customuser": user,
                "code": code_model.tokens,
                "link": host_address,
                "hour": 32,
            })

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [f"{user.email}", ]

            email_msg = EmailMessage(
                subject = f"{name}: Email Activation",
                body = message,
                from_email = email_from,
                to = recipient_list,
            )

            try:
                email_msg.content_subtype = "html"
                email_msg.send()
            except: pass

            return Response({
                "status": "ok",
            })

            
        if change_type == "phone":
            if m02_users.CustomUser.objects.filter(phone = old_phone).count() == 0:
                return Response({
                    "status": "error",
                    "code": "phone_not_found",
                })
            
            user                        = m02_users.CustomUser.objects.get(phone = old_phone)
            user.phone                  = phone
            user.save()
            
            if m02_users.EmailPhoneConfirmation.objects.filter(
                user = user,
                method = change_type,
                exp_date__gt = datetime.date.today(),
            ).count() > 0:
                code_model = m02_users.EmailPhoneConfirmation.objects.get(
                    user = user,
                    method = change_type,
                    exp_date__gt = datetime.date.today(),
                )

                code_model.sms_count += 1
                code_model.save()

                if code_model.sms_count > 3:
                    return Response({
                        "status": "error",
                        "code": "sms_reached",
                    })
                
            else:

                code                        = crypto.get_random_string(6, "0123456789")
                code_model                  = m02_users.EmailPhoneConfirmation()
                code_model.user             = user
                code_model.method           = change_type
                code_model.exp_date         = datetime.timedelta(hours=32) + datetime.date.today()
                code_model.tokens           = code
                code_model.sms_count        = 1
                code_model.save()
    
            message = f"Phone number activation code is: {code_model.tokens}\nRemember This code is valid for 24 hours."

            # Some kind of code to call sms sending api

            return Response({
                "status": "ok",
            })
        
        return Response({
            "status": "ok",
        })
    
    # Get Notifications
    def get_notifications(self, request):
        tokens = request.data.get("tokens")
        token_model = m02_users.AuthTokens.objects.filter(tokens=tokens)
        if token_model.count() == 0:
            return Response({
                "status": "error",
                "code": "token_expired",
            })
        
        user = token_model.first().user
        
        notifications = m02_users.UserNotification.objects.filter(
            user = user,
        ).order_by("-id")

        notifications = Paginator(notifications, 10).get_page(1)

        notifications_serializer = s02_user.NotificationSerializer(notifications, many = True)
        
        return Response({
            "status": "ok",
            "data": notifications_serializer.data,
        })
        
    def send_activation(self, request):
        subject = '{{ name }}: User Activation'
        message = render_to_string("accounts/activation_code.html", )
        
        message = strip_tags(message)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ["{user.email}", ]
        send_mail(subject, message, email_from, recipient_list, True)














