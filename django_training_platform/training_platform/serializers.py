from rest_framework import serializers

from . import models as m


# class OwnerTrackingModelSerializer(serializers.ModelSerializer):
#     """
#     https://github.com/encode/django-rest-framework/pull/5886
#     https://github.com/encode/django-rest-framework/issues/6031
#     Carrying request.user data deeper into serializer
#
#     Assuming model has owner field
#     """
#     owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
#
#     def save(self, **kwargs):
#         """Include default for read_only `user` field"""
#         kwargs["owner"] = self.fields["owner"].get_default()
#         return super().save(**kwargs)


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Membership
        fields = ["course", "user", "owner"]
        read_only_fields = ["owner"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Course
        fields = "__all__"
        read_only_fields = ["owner"]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Lesson
        fields = "__all__"
        read_only_fields = ["owner"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Task
        fields = "__all__"
        read_only_fields = ["owner"]


class CompletedTaskSerializer(serializers.ModelSerializer):
    grade_present = serializers.BooleanField(read_only=True)

    class Meta:
        model = m.CompletedTask
        fields = ["id", "owner", "content", "task", "grade_present"]
        read_only_fields = ["owner", ]


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Grade
        fields = "__all__"
        read_only_fields = ["owner"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Comment
        fields = "__all__"
        read_only_fields = ["owner"]
