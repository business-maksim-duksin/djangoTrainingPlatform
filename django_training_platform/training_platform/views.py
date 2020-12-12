from rest_framework import generics, permissions, viewsets, mixins

from .models import Course
from .permissions import IsTeacher, IsObjOwner, IsCourseMemberOrOwner, IsCourseMemberOrOwner, IsLessonRelatedToCourse,\
    IsTaskRelatedToCourse,  IsCompletedTaskRelatedToCourse, IsGradeRelatedToCourse, IsCommentRelatedToCourse
from .serializers import (
    UserSerializer,
    CourseSerializer,
    LessonSerializer,
    TaskSerializer,
    # CourceSerializer2,
    # CourceSerializer3,

)

from . import serializers as s
from . import models as m

from .mixins import OwnerPerformCreateMixin


class UserCreateView(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class MembershipView(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """Membership which gains access to course"""
    serializer_class = s.MembershipSerializer
    queryset = m.Membership.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class CourseView(OwnerPerformCreateMixin,
                 viewsets.ModelViewSet):
    """Course"""
    serializer_class = s.CourseSerializer
    queryset = m.Course.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        create(), retrieve(), update(), partial_update(), destroy() and list()
        """
        if self.action == "create":
            permission_classes = [permissions.IsAuthenticated, IsTeacher]
        elif self.action in ["retrieve", "list"]:
            permission_classes = [permissions.IsAuthenticated, IsCourseMemberOrOwner]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated, IsObjOwner]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class LessonView(OwnerPerformCreateMixin,
                 viewsets.ModelViewSet):
    """Lesson"""
    serializer_class = LessonSerializer
    queryset = m.Lesson.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        create(), retrieve(), update(), partial_update(), destroy() and list()
        """
        if self.action == "create":
            permission_classes = [permissions.IsAuthenticated, IsTeacher, IsLessonRelatedToCourse]
        elif self.action in ["retrieve", "list"]:
            permission_classes = [permissions.IsAuthenticated, IsCourseMemberOrOwner]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated, IsObjOwner]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class TaskView(OwnerPerformCreateMixin,
               viewsets.ModelViewSet):
    """Task"""
    serializer_class = TaskSerializer
    queryset = m.Task.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        create(), retrieve(), update(), partial_update(), destroy() and list()
        """
        if self.action == "create":
            permission_classes = [permissions.IsAuthenticated, IsTeacher, IsTaskRelatedToCourse]
        elif self.action in ["retrieve", "list"]:
            permission_classes = [permissions.IsAuthenticated, IsCourseMemberOrOwner]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated, IsObjOwner]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class CompletedTaskView(OwnerPerformCreateMixin,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """Completed task"""
    serializer_class = s.CompletedTaskSerializer
    queryset = m.CompletedTask.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        create(), retrieve(), update(), partial_update(), destroy() and list()
        """
        if self.action == "create":
            permission_classes = [permissions.IsAuthenticated, IsCompletedTaskRelatedToCourse]
        elif self.action in ["retrieve", "list"]:
            permission_classes = [permissions.IsAuthenticated, IsCourseMemberOrOwner]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class GradeView(OwnerPerformCreateMixin,
                mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    """Grade of the completed task"""
    serializer_class = s.GradeSerializer
    queryset = m.Grade.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        create(), retrieve(), update(), partial_update(), destroy() and list()
        """
        if self.action == "create":
            permission_classes = [permissions.IsAuthenticated, IsTeacher, IsGradeRelatedToCourse]
        elif self.action in ["retrieve", "list"]:
            permission_classes = [permissions.IsAuthenticated, IsCourseMemberOrOwner]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class CommentView(OwnerPerformCreateMixin,
                  viewsets.ModelViewSet):
    """Comment for a grade"""
    serializer_class = s.GradeSerializer
    queryset = m.Grade.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        create(), retrieve(), update(), partial_update(), destroy() and list()
        """
        if self.action == "create":
            permission_classes = [permissions.IsAuthenticated, IsTeacher, IsCommentRelatedToCourse]
        elif self.action in ["retrieve", "list"]:
            permission_classes = [permissions.IsAuthenticated, IsCourseMemberOrOwner]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated, IsObjOwner]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]
