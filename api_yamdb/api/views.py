from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from .filters import TitleFilter
from .mixins import CreateDestroyListViewSet
from .permissions import IsAdminModerAuthorOrReadOnly, ListAllModerAdminOnly
from .serializers import AddTitleSerializer, CategorySerializer
from .serializers import CommentSerializer, GenreSerializer, ReviewSerializer
from .serializers import TitleSerializer
from reviews.models import Category, Comment, Genre, Review, Title


class CategoryViewSet(CreateDestroyListViewSet):
    """Вьюсет для модели категорий."""
    queryset = Category.objects.order_by('id')
    serializer_class = CategorySerializer


class GenreViewSet(CreateDestroyListViewSet):
    """Вьюсет для модели жанров."""
    queryset = Genre.objects.order_by('id')
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели произведений."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = AddTitleSerializer
    permission_classes = (ListAllModerAdminOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return AddTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModerAuthorOrReadOnly]

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModerAuthorOrReadOnly]

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        return Comment.objects.filter(review=review)
