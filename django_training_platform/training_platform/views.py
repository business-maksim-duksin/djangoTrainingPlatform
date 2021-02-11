from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions, viewsets, mixins
from django.db.models import Q, Count, Exists, OuterRef, Subquery

from core.permissions import IsTeacher, IsObjOwner, IsCourseMemberOrOwner, IsLessonRelatedToCourse, \
    IsTaskRelatedToCourse, IsCompletedTaskRelatedToCourse, IsGradeRelatedToCourse, IsCommentRelatedToCourse, \
    IsMembershipRelatedToCourse

from . import serializers as s
from . import models as m

from .mixins import OwnerPerformCreateMixin


class MembershipView(OwnerPerformCreateMixin,
                     mixins.CreateModelMixin,
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
            permission_classes = [permissions.IsAuthenticated, IsTeacher, IsCourseMemberOrOwner]
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
    filter_backends = [filters.SearchFilter, ]
    search_fields = ["name", "description"]

    def get_queryset(self):
        """Member of the course or it's creator"""
        user = self.request.user
        # return self.queryset.filter(
        #                             Q(memberships__user=user) |
        #                             Q(owner=user)
        #                             )
        user_subscribed_courses_qs = Subquery(m.Membership.objects.all().filter(user=user).values('course'))
        return self.queryset.filter(
                                    Q(id__in=user_subscribed_courses_qs) |
                                    Q(owner=user)
                                    )
        # sub_queryset_2 =
        # return sub_queryset_1

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["course", ]
    search_fields = ["name", ]

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["lesson", ]
    search_fields = ["content", ]

    def get_queryset(self):
        """All tasks of courses where user is it's member or user is creator of the course. """
        user = self.request.user
        return self.queryset.filter(Q(course__memberships__user=user) |
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
    queryset = m.CompletedTask.objects.all() \
        .annotate(grade_present=Exists(m.Grade.objects.filter(completed_task=OuterRef('pk'))))
    permission_classes = (permissions.IsAuthenticated,)

    # filter_backends = [DjangoFilterBackend]    # INVESTIGATE
    # filterset_fields = ["grade_present", ]  #TypeError: 'Meta.fields' must not contain non-model field names: grade_present

    def get_queryset(self):
        """
        User is teacher:
            all completed tasks where teacher is a member of the course.
        User is student:
            user's own completed tasks.
        """
        user = self.request.user
        if user.is_teacher:
            queryset = self.queryset.filter(course__memberships__user=user)
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
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ["completed_task", "amount"]

    def get_queryset(self):
        """
        User is teacher:
           all grades in associated courses where teacher is still a member
        User is student:
            all grades for student's completed_tasks
        """
        user = self.request.user
        if user.is_teacher:
            queryset = self.queryset.filter(course__memberships__user=user)
        else:
            queryset = self.queryset.filter(completed_task__owner=user)
        return queryset

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
    serializer_class = s.CommentSerializer
    queryset = m.Comment.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["grade", ]
    search_fields = ["content", ]

    def get_queryset(self):
        """
        User is teacher:
           all comments associated with teachers grades
        User is student:
            all comments derived from student's completed_tasks
        """
        user = self.request.user
        if user.is_teacher:
            queryset = self.queryset.filter(grade__owner=user)
        else:
            queryset = self.queryset.filter(grade__completed_task__owner=user)
        return queryset

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
