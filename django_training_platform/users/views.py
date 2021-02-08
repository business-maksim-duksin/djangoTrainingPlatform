from rest_framework import generics, permissions
from . import serializers as s



# Create your views here.
class UserCreateView(generics.CreateAPIView):
    serializer_class = s.UserSerializer
    permission_classes = (permissions.AllowAny,)

