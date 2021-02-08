from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserCreateView, UserListView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'users'

urlpatterns = [
    path('register', UserCreateView.as_view()),
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    # path('users', UserListView.as_view()),
]

router = DefaultRouter()
router.register(r"users", UserListView)
urlpatterns += [
    path('', include(router.urls)),
]
