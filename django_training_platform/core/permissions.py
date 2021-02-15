from rest_framework import permissions
from training_platform.models import OwnedModel, CourseScopeModelInterface, Course, Lesson, Task, CompletedTask, Grade, Comment, Membership
from django.contrib.auth import get_user_model


class IsTeacher(permissions.BasePermission):
    message = "You have to be a Teacher to perform this action."

    def has_permission(self, request, view):
        return bool(request.user.is_teacher or request.user.is_staff)


class IsObjOwner(permissions.BasePermission):
    message = "You have to be an Owner to perform this action."

    def has_object_permission(self, request, view, obj: OwnedModel):
        # Instance must have an attribute named `owner`.
        return bool(obj.owner == request.user or request.user.is_staff)


class IsCourseMemberOrOwner(permissions.BasePermission):
    message = "You have to be a Member of the course to perform this action."

    def has_object_permission(self, request, view, obj: CourseScopeModelInterface):
        # course = Course.objects.select_related('memberships').get(id=obj)
        return bool(obj.course.memberships.filter(user=request.user).exists() or
                    obj.course.owner == request.user)
        # return bool(course.memberships.filter(user=request.user).exists() or
        #             course.owner == request.user)


class IsObjRelatedToCourseBase(permissions.BasePermission):
    """
    Base class to spawn per-model permissions for CourseScopeModelInterface models.
    The permission itself checks if user is a Member of a corresponding Course when trying to POST an obj.

    I could do dynamic class construction, but it is too scary for me for now.
    """
    message = "User is not a Member of the Course. "

    # def __init__(self, obj: CourseScopeModelInterface, foreign_key: str):
    #     self.obj = obj
    #     self.foreign_key = foreign_key
    #     self.message = f"{self.obj} does not belong to course_id {self.foreign_key}"

    def has_permission(self, request, view, obj: CourseScopeModelInterface, foreign_key: str):
        foreign_key = "course"
        foreign_key_id = request.data.get(foreign_key)
        if foreign_key_id:
            # course_ins = Course.objects.all().select_related("owner").get(id=foreign_key_id)
            # user_id = request.user.id
            # user = get_user_model().objects.get(id=user_id)
            # return bool(course_ins.memberships.filter(user=user).exists() or
            #             course_ins.owner == user)

            # obj = Course
            # course_ins = Course.objects.get(id=foreign_key_id)
            # return bool(course_ins.memberships.filter(user=request.user).exists() or
            #             course_ins.owner == request.user)

            # obj = Course
            # return bool(obj.objects.get(id=foreign_key_id).memberships.filter(user=request.user).exists() or
            #             obj.objects.get(id=foreign_key_id).owner == request.user)

            # obj = Course
            # return bool(obj.objects.all().filter(id=foreign_key_id).filter(memberships__user=request.user).exists() or
            #             obj.objects.get(id=foreign_key_id).owner == request.user)

            return bool(Membership.objects.all().filter(user=request.user).filter(course__id=foreign_key_id).exists() or
                        Course.objects.get(id=foreign_key_id).owner == request.user)
        else:
            return False


class IsLessonRelatedToCourse(IsObjRelatedToCourseBase):
    """
    I could do dynamic class construction, but it is too scary for me for now.
    Or i don't understand how perform this check properly.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view, Course, "course",)
        # obj = Lesson
        # foreign_key = "course"
        # foreign_key_id = request.data.get(foreign_key)
        # if foreign_key_id:
        #     return bool(obj.objects.get(id=foreign_key_id).get_associated_course.memberships.filter(user=request.user).exists())
        # else:
        #     return False


class IsTaskRelatedToCourse(IsObjRelatedToCourseBase):
    """
    I could do dynamic class construction, but it is too scary for me for now.
    Or i don't understand how perform this check properly.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view, Lesson, "lesson",)


class IsCompletedTaskRelatedToCourse(IsObjRelatedToCourseBase):
    """
    I could do dynamic class construction, but it is too scary for me for now.
    Or i don't understand how perform this check properly.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view, Task, "task", )


class IsGradeRelatedToCourse(IsObjRelatedToCourseBase):
    """
    I could do dynamic class construction, but it is too scary for me for now.
    Or i don't understand how perform this check properly.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view, CompletedTask, "completed_task", )

class IsCommentRelatedToCourse(IsObjRelatedToCourseBase):
    """
    I could do dynamic class construction, but it is too scary for me for now.
    Or i don't understand how perform this check properly.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view, Grade, "grade", )


class IsMembershipRelatedToCourse(IsObjRelatedToCourseBase):
    """
    I could do dynamic class construction, but it is too scary for me for now.
    Or i don't understand how perform this check properly.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view, Course, "course", )