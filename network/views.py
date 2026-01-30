from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .models import NetworkNode
from .permissions import IsActiveEmployee
from .serializers import NetworkNodeSerializer


class NetworkNodeViewSet(ModelViewSet):
    queryset = (
        NetworkNode.objects
        .select_related("supplier")
        .prefetch_related("products")
    )
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("country",)
