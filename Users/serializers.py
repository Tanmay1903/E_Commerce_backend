from rest_framework_mongoengine import serializers,generics
from django_mongoengine.mongo_auth.managers import get_user_document
from rest_framework_mongoengine.fields import ObjectIdField

User = get_user_document()

class UserCreateSerializer(serializers.DocumentSerializer):
    class Meta:
        model=User
        fields = ('first_name','last_name','username','email','password')
        extra_kwargs={
                        "password":{"write_only": True}
        }

    def validate_email(self,data):
        user_qs = User.objects.filter(email=data)
        if user_qs:
            raise generics.ValidationError()
        return data

    def create(self,validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = validated_data['username']
        email = validated_data['email'].lower()
        password = validated_data['password']
        user_obj = User(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                password = password
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class UserLoginSerializer(serializers.DocumentSerializer):
    class Meta:
        model = User
        fields = ('email','password')
        extra_kwargs={
                        "password":{"write_only": True}
        }

    def validated_data(self,data):
        user_obj = None
        email = data.get("email",None)
        email = email.lower()
        password = data["password"]
        if not email:
            raise generics.ValidationError("A Email is required to login.")

        user = User.objects.filter(
            email=email
        )
        if user and user.count() == 1:
            user_obj=user.first()
        else:
            raise generics.ValidationError("This Email is not valid!")
        if user_obj:
            if not user_obj.check_password(password):
                raise generics.ValidationError("Incorrect credentials please try again.")
        return user_obj

class UserLogoutSerializer(serializers.DocumentSerializer):
    class Meta:
        model=User
        fields = ()


# harshita
class UserSerializer(serializers.DocumentSerializer):
    userid = ObjectIdField(source = 'id')
    class Meta():
        model=User
        fields=("userid","first_name","last_name","address","phone_no","email","username")
