from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.common_utils.constant import ERROR_TEXT
from apps.common_utils.functions import get_random_integer
from apps.models import User
from apps.models.tags import TagToUser
from apps.models.users import UserRecovery


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['password', 'username', 'name', 'last_name', 'email', 'birthday']

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
        fields = ['username', 'name', 'last_name', 'email', 'password', 'birthday']

    def update(self, instance, validated_data):
        new_password = validated_data.pop('password', None)
        update_instance = super(UserShortSerializer, self).update(instance, validated_data)
        if new_password:
            update_instance.set_password(new_password)
            update_instance.save()
        return update_instance


@extend_schema_serializer(exclude_fields=['user'])
class UserStartRecoverySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    user = serializers.IntegerField(read_only=True)
    message = serializers.CharField(read_only=True, default='check your e-mail')

    class Meta:
        model = UserRecovery
        fields = ['email', 'user', 'message']

    def validate(self, attrs):
        email = attrs.get('email')
        if email:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError({'email': ERROR_TEXT.get('email_exist')})
        return attrs

    def create(self, validated_data):
        user = User.objects.get(email=validated_data.get('email'))
        code = get_random_integer(6)
        store_code = make_password(code)
        user_recovery, _ = UserRecovery.objects.get_or_create(user=user)
        user_recovery.code = store_code
        user_recovery.save()
        subject = 'Password recovery'
        message = f'It is okay sometimes forget password, ' \
                  f'take this code: {code} ' \
                  f'enter and enjoy your day'
        email_from = settings.EMAIL_HOST_USER

        recipient_list = [validated_data.pop('email', None), ]
        try:
            send_mail(subject, message, email_from, recipient_list)
        except SMTPException:
            raise ParseError({'message': 'error has occurred while send code on this email'})

        return {'message': 'check your e-mail'}


class UserFinishRecoverySerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'code', 'password']

    def create(self, validated_data):
        new_password = validated_data.pop('password', None)
        try:
            instance = User.objects.get(email=validated_data.get('email'))
        except User.DoesNotExist:
            raise ParseError('user not found')
        try:
            instance_recovery = UserRecovery.objects.get(user=instance)
        except UserRecovery.DoesNotExist:
            raise ParseError('recovery process does not started')
        if check_password(validated_data.get('code'), instance_recovery.code):
            instance.set_password(new_password)
            instance.save()
            instance_recovery.delete()
        return instance


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
