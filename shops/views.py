from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from books.models import Publisher
from .models import BookShop, Sale
from .serializers import BookShopSerializer, SaleSerializer


class ShopView(generics.ListAPIView):
    serializer_class = BookShopSerializer
    permission_classes = (AllowAny,)
    queryset = BookShop.objects.all()

    def get_object(self):
        publisher_id = self.kwargs['publisher_pk']
        return get_object_or_404(Publisher.objects.all(), pk=publisher_id)

    def get_queryset(self):
        publisher = self.get_object()
        return BookShop.objects.filter(
            stock__book__publisher_id=publisher.id,
            sale__book__publisher=publisher.id
        ).distinct()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['publisher'] = self.get_object()
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            dict(shops=[shop for shop in sorted(serializer.data, key=lambda x: x['books_sold_count'])])
        )


class SaleVew(generics.ListCreateAPIView):
    serializer_class = SaleSerializer
    permission_classes = (AllowAny,)
    queryset = Sale.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('shop', 'book')
