from rest_framework import generics, permissions, viewsets, mixins
from django.db.models import Q, Count

from .permissions import IsTeacher, IsObjOwner, IsCourseMemberOrOwner, IsLessonRelatedToCourse, \
    IsTaskRelatedToCourse, IsCompletedTaskRelatedToCourse, IsGradeRelatedToCourse, IsCommentRelatedToCourse, \
    IsMembershipRelatedToCourse

from . import serializers as s
from . import models as m

from .mixins import OwnerPerformCreateMixin


class UserCreateView(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = s.UserSerializer
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

    def get_queryset(self):
        """User's memberships"""
        user = self.request.user
        return self.queryset.filter(user=user)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        create(), retrieve(), update(), partial_update(), destroy() and list()
        """
        if self.action == "create":
            permission_classes = [permissions.IsAuthenticated, IsTeacher, IsMembershipRelatedToCourse]
        elif self.action in ["retrieve", "list"]:
            permission_classes = [permissions.IsAuthenticated, IsCourseMemberOrOwner]
        elif self.action in ["destroy"]:
            permission_classes = [permissions.IsAuthenticated, IsTeacher, IsCourseMemberOrOwner]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class CourseView(OwnerPerformCreateMixin,
                 viewsets.ModelViewSet):
    """Course"""
    serializer_class = s.CourseSerializer
    queryset = m.Course.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Member of the course or it's creator"""
        user = self.request.user
        return self.queryset.filter(Q(memberships__user=user) |
                                    Q(owner=user))

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
    serializer_class = s.LessonSerializer
    queryset = m.Lesson.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """All lessons of courses where user is it's member or user is creator of the course. """
        user = self.request.user
        return self.queryset.filter(Q(course__memberships__user=user) |
                                    Q(owner=user))

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
    serializer_class = s.TaskSerializer
    queryset = m.Task.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """All tasks of courses where user is it's member or user is creator of the course. """
        user = self.request.user
        return self.queryset.filter(Q(lesson__course__memberships__user=user) |
                                    Q(owner=user))

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
    # for some reason Exists('grade') gives AttributeError: 'str' object has no attribute 'order_by'  # INVESTIGATE
    queryset = m.CompletedTask.objects.all().annotate(grade_present=Count('grade'))
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        User is teacher:
            all completed tasks where teacher is a member of the course.
        User is student:
            user's own completed tasks.
        """
        user = self.request.user
        if user.is_teacher:
            queryset = self.queryset.filter(task__lesson__course__memberships__user=user)
        else:
            queryset = self.queryset.filter(owner=user)
        return queryset

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
