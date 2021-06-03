import re
from django.shortcuts import render,redirect
from rest_framework_mongoengine.generics import CreateAPIView, GenericAPIView, ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from rest_framework import status
from .serializers import UserLoginSerializer, UserCreateSerializer, UserLogoutSerializer, UserSerializer, \
ResendVerificationSerializer, EmailUpdateSerializer, PasswordSerializer, Passwordupdateserializer, FirstNameSerializer,LastNameSerializer, \
    AddressSerializer, AddressUpdateSerializer
from django.contrib.auth import login, logout
from .auth import IsAuthenticated
from django_mongoengine.mongo_auth.managers import get_user_document
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

User = get_user_document()

class UserRegister(CreateAPIView):
    '''
    An api for the customers(general public)
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

                user = User.objects.get(username=username)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your Sparkcart account.'
                message = render_to_string('Product/account_activation_email_api.html', {
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
            else:
                return Response({"message":"email does not exist"}, status=status.HTTP_409_CONFLICT)
        except ValidationError:
            return Response({"message":"This Email is already registered.Please login to your account."}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def act(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        user.backend = 'django_mongoengine.mongo_auth.backends.MongoEngineBackend'
        login(request, user , backend=user.backend)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

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
                            {"message":"To Login,please click on the verification link sent to you on your registered email"}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({"message":"Invalid login details"}, status = status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
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

class ResendVerificationAPI(CreateAPIView):
    '''
    an api for the users to resend verification link
    '''
    serializer_class = ResendVerificationSerializer

    def post(self, request):

        data = request.data
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message":"User does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = User.objects.get(email=email)
        except User.DoesNotExist:
            instance = None
        serializer = ResendVerificationSerializer(instance, data=data)
        try:
            if serializer.is_valid():
                if not user.is_active:
                    current_site = get_current_site(request)
                    subject = 'Activate Your Sparkcart Account'
                    message = render_to_string('Product/account_activation_email_api.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    to_email = request.data.get('email')
                    email = EmailMultiAlternatives(
                        subject, message, to=[to_email]
                    )
                    email.attach_alternative(message, 'text/html')
                    email.send()
                    return Response({"message":"Account activation link sent to your email"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message":"User is already Verified"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class EmailupdateAPI(CreateAPIView):
    '''
    an api for the users to update their email address.
    '''
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailUpdateSerializer

    def post(self, request):

        data = request.data
        email = request.user.email
        new_email = request.data.get('new_email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message":"User does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = User.objects.get(email=email)
        except User.DoesNotExist:
            instance = None
        serializer = EmailUpdateSerializer(instance, data=data)
        try:
            if serializer.is_valid():
                user.email = new_email
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate Your Sparkcart Account'
                message = render_to_string('Product/account_activation_email_api.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = request.user.email
                email = EmailMultiAlternatives(
                    subject, message, to=[to_email]
                )
                email.attach_alternative(message, 'text/html')
                email.send()
                return Response({"message":"Email updated please verify to confirm account"}, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        email = request.data.get('email')
        email = email.lower()
        try:
            instance = User.objects.get(email=email)
        except User.DoesNotExist:
            instance = None
        serializer = PasswordSerializer(instance, data=data)
        #try:
        if serializer.is_valid():
            user = User.objects.get(email=email)
            current_site = get_current_site(request)
            mail_subject = 'Change your Sparkcart account password.'
            message = render_to_string('Product/password_change_api.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            message = re.sub('/api/', '/', message)
            to_email = request.data.get('email')
            email = EmailMultiAlternatives(
                mail_subject, message, to=[to_email]
            )
            email.attach_alternative(message, 'text/html')
            email.send()
            return Response({"message": "Password reset e-mail has been sent."},
                            status=status.HTTP_200_OK)
        else:
            return Response({"message": "email does not exist"}, status=status.HTTP_409_CONFLICT)
        #except :
        #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Passwordupdateview(GenericAPIView):
    """
    An API to update Password of already existed user
    """

    serializer_class = Passwordupdateserializer

    def post(self,request,uidb64,token):
        data = request.data
        password = request.data.get('password')
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        try:
            instance = User.objects.get(email=user.email)
        except User.DoesNotExist:
            instance = None
        serializer = Passwordupdateserializer(instance, data=data)
        try:
            if serializer.is_valid():
                if user is not None and account_activation_token.check_token(user, token):
                    if user.username == password:
                        return Response({"message":"Username and new password should be different"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        user.set_password(password)
                        user.save()
                        return Response({"message":"successfully password change"}, status=status.HTTP_200_OK)
                else:
                    return HttpResponse('Activation link is invalid!')
        except ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class update_firstname(GenericAPIView):
    serializer_class = FirstNameSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()

    def post(self,request):
        data = request.data
        Email = request.user.email
        serializer = FirstNameSerializer(data=data)
        if serializer.is_valid():
            User.objects.filter(email=Email).update(first_name=data['first_name'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class update_lastname(GenericAPIView):
    serializer_class = LastNameSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()

    def post(self,request):
        data = request.data
        Email = request.user.email
        serializer = LastNameSerializer(data=data)
        if serializer.is_valid():
            User.objects.filter(email=Email).update(last_name=data['last_name'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class AddressView(CreateAPIView):
    '''
    An api for the user to add address
    '''
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        email = request.user.email
        add = request.data.get('address')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message":"User does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AddressSerializer(user, data=data)
        try:
            if serializer.is_valid():
                if len(user.address) == 4:
                    return Response({"message":"delete an address to add new one"},status = status.HTTP_409_CONFLICT)
                else:
                    l = []
                    l.append(add["address"])
                    for i in user.address:
                        l.append(user.address[i])
                    for i in range(len(l)):
                        user.address[str(i)] = l[i]
                    user.save()
                    return Response({"message":"address succesfully saved"}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Addressdeleteview(CreateAPIView):
    '''
    An api for the user to delete address
    '''
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        data = request.data
        email=request.user.email
        add = request.data.get('address')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message":"User does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AddressSerializer(user, data=data)
        try:
            if serializer.is_valid():
                for i in user.address:
                    if user.address[i]==add["address"]:
                        del user.address[i]
                        user.save()
                        return Response({"message":"successfully deleted"}, status=status.HTTP_200_OK)
                return Response({"message":"address not found"},status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class Addresslistview(GenericAPIView):
    '''
    An api for the user to show the addresses
    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(request.user.address,status=status.HTTP_200_OK)

class Addressupdateview(CreateAPIView):
    '''
    An api for the customer to update the address
    '''
    serializer_class = AddressUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(request.user.address,status=status.HTTP_200_OK)

    def post(self,request):
        data = request.data
        email=request.user.email
        new_add=request.data.get('new_address')
        add = request.data.get('address')
        user = User.objects.get(email=email)
        serializer = AddressUpdateSerializer(user, data=data)
        try:
            if serializer.is_valid():
                for i in user.address:
                    if user.address[i]==add["address"]:
                        user.address[i] = new_add
                        user.save()
                        return Response({"message":"Address updated successfully."},status=status.HTTP_200_OK)
                return Response({"message":"address not found for update"},status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)