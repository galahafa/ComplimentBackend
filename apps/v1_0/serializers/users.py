from django.contrib.auth.password_validation import validate_password
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.common_utils.constant import ERROR_TEXT
from apps.models import User
from apps.models.tags import TagToUser


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['password', 'password2', 'username', 'name', 'last_name', 'email']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": ERROR_TEXT.get('password_compare')})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            last_name=validated_data.get('last_name')
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'name', 'last_name', 'email']


@extend_schema_serializer(exclude_fields=['user'])
class TagToUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TagToUser
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }

        user_obj = (User.objects.filter(email=attrs.get("username")).first() or
                    User.objects.filter(username=attrs.get("username")).first())
        if user_obj:
            credentials['username'] = user_obj.username

        return super().validate(credentials)

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
