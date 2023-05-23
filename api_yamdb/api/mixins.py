from rest_framework import filters, mixins, viewsets

from .permissions import ListAll_ModerAdminOnly


class CreateDestroyListViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Миксовый дженерик для операций вьюсетов категорий и жанров."""
    permission_classes = (ListAll_ModerAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
