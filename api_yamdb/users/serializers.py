from rest_framework import serializers

from .models import User
from .validators import validate_email, validate_username


class RegisterUserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации."""
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username, ],
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[validate_email, ],
        required=True
    )

    class Meta:
        fields = ('username', 'email', )
        model = User


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username, ],
        required=True
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username, ],
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[validate_email, ],
    )

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User


class UserEditSerializer(UserSerializer):
    """Сериализатор для редактирования."""
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
        read_only_fields = ['role', ]
