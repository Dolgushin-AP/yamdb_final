from api.permissions import IsAdmin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import (RegisterUserSerializer, TokenSerializer,
                          UserEditSerializer, UserSerializer)


def send_mail_with_code(user):
    """Отправка письма с кодом подтверждения."""
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Confirmation code',
        message=f'Code: {confirmation_code}',
        recipient_list=[user.email, ],
        from_email=None
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_register(request):
    """Регистрация пользователя и отправка кода подтверждения."""
    serializer = RegisterUserSerializer(data=request.data)
    if User.objects.filter(username=request.data.get('username'),
                           email=request.data.get('email')).exists():
        user = User.objects.get(
            username=request.data.get('username'))
        send_mail_with_code(user)
        return Response('Код изменен')

    if serializer.is_valid():
        serializer.save()
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        send_mail_with_code(user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """Получения JWT-токена."""
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        confirmation_code = serializer.validated_data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели пользователя."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [IsAdmin, ]
    filter_backends = (SearchFilter, )
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='get_me',
        permission_classes=[IsAuthenticated, ]
    )
    def get_me_profile(self, request):
        if request.method == 'PATCH':
            serializer = UserEditSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(
        methods=['get', 'patch', 'delete', ],
        detail=False,
        url_path=r'(?P<username>\w+)',
        url_name='get_user'
    )
    def get_user_by_user_name(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(user)
        return Response(serializer.data)
