from rest_framework import viewsets, permissions
from booking.models import Category
from booking.serializers import category_serializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = category_serializer.CategorySerializer
    permission_classes = [permissions.AllowAny]