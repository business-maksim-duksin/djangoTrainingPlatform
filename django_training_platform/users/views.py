from rest_framework import generics, permissions
from rest_framework import permissions, viewsets, mixins
from . import serializers as s
from core.permissions import IsTeacher
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

# from django.conf import settings
# User = settings.AUTH_USER_MODEL


# Create your views here.
class UserCreateView(generics.CreateAPIView):
    serializer_class = s.UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = s.UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (permissions.IsAuthenticated, IsTeacher)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'first_name', 'last_name', 'is_teacher']

