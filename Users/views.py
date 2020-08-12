from django.shortcuts import render,redirect
from rest_framework_mongoengine.generics import CreateAPIView, GenericAPIView, ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import UserLoginSerializer, UserCreateSerializer, UserLogoutSerializer, UserSerializer
from django.contrib.auth import login, logout
from .auth import IsAuthenticated
from django_mongoengine.mongo_auth.managers import get_user_document

User = get_user_document()

class UserRegister(CreateAPIView):
    '''
    An api for the customers(genral public)
    to register themselves. Once the customers register
    themselves an email verification link will be send to them to complete the registeration
    process.
    '''
    serializer_class = UserCreateSerializer

    def get_queryset(self):
        return User.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        username = request.data.get('username')
        email = request.data.get('email').lower()
        try:
            user = User.objects.get(username=username)
            if user:
                raise ValidationError()
        except User.DoesNotExist:
            user = None
        except ValidationError:
            return Response({"message":"Username is already taken."}, status=status.HTTP_409_CONFLICT)
        try:
            instance = User.objects.get(email=email)
        except User.DoesNotExist:
            instance = None
        serializer = UserCreateSerializer(instance, data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                '''
                user = User.objects.get(username=username)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your 9eye.in account.'
                message = render_to_string('stores/account_activation_email_api.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })

                to_email = request.data.get('email').lower()
                email = EmailMultiAlternatives(
                    mail_subject, message, to=[to_email]
                )
                email.attach_alternative(message, 'text/html')
                email.send()
                return Response({"message":"Please confirm your email address to complete the registration"},status=status.HTTP_200_OK)
                '''
                return Response(serializer.validate_email(data),status=status.HTTP_201_CREATED)
            else:
                return Response({"message":"email does not exist"}, status=status.HTTP_409_CONFLICT)
        except ValidationError:
            return Response({"message":"This Email is already registered.Please login to your account."}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(GenericAPIView):
    '''
    An api for the customers to login
    '''
    serializer_class = UserLoginSerializer

    def get_queryset(self):
        return User.objects.all()


    def post(self, request, *args, **kwargs):
        data = request.data
        email = request.data.get('email')
        email = email.lower()
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response("User does not exist!", status=status.HTTP_204_NO_CONTENT)
        try:
            instance = User.objects.get(email=email)
        except User.DoesNotExist:
            instance = None
        serializer = UserLoginSerializer(instance, data=data)
        try:
            if serializer.is_valid():
                if user.check_password(password):
                    if user.is_active:
                        user.backend = 'django_mongoengine.mongo_auth.backends.MongoEngineBackend'
                        login(request, user, backend=user.backend)
                        user_obj = serializer.validated_data(data)
                        user_data = User.objects.get(email=str(user_obj))
                        user_data = User.json(user_data,str(user_data['id']))
                        return Response(user_data, status=status.HTTP_200_OK)
                    else:
                        return Response(
                            "To Login,please click on the verification link sent to you on your registered email", status=status.HTTP_202_ACCEPTED)
                else:
                    return Response("Invalid login details", status = status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(GenericAPIView):
    '''
    An api for the customers to logout
    '''
    permission_classes = (IsAuthenticated,)
    serializer_class = UserLogoutSerializer


    def post(self, request):
        logout(request)
        response = Response({"message":"You have been successfully logged out"},status=status.HTTP_200_OK)
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')
        return response



class Userlist(GenericAPIView):
    '''
    An api which displays list of all the customers
    '''
    def get(self, request):
        if request.method == "GET":
            users1 = User.objects.all()
            serial = UserSerializer(users1, many=True)
            return Response(serial.data)

    def get_queryset(self):
        return User.objects.all()
