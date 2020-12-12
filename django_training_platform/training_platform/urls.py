"""django_training_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # path("course", views.CourceView.as_view()),
    path('register', views.UserCreateView.as_view()),
    # path('lesson', views.LessonView.as_view()),
    # path('task', views.TaskView.as_view()),

]

from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"memberships", views.MembershipView)
router.register(r"courses", views.CourseView)
router.register(r"lessons", views.LessonView)
router.register(r"tasks", views.TaskView)
router.register(r"completed_tasks", views.CompletedTaskView)
router.register(r"grades", views.GradeView)
router.register(r"comments", views.CommentView)


# The API URLs are now determined automatically by the router.
urlpatterns += [
    path('', include(router.urls)),
]
