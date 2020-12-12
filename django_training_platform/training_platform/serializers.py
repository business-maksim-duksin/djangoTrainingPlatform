from rest_framework import serializers

from .models import Course, User, Lesson, Task
from . import models as m


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password", "is_teacher")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class OwnerTrackingModelSerializer(serializers.ModelSerializer):
    """
    https://github.com/encode/django-rest-framework/pull/5886
    https://github.com/encode/django-rest-framework/issues/6031
    Carrying request.user data deeper into serializer

    Assuming model has owner field
    """
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    def save(self, **kwargs):
        """Include default for read_only `user` field"""
        kwargs["owner"] = self.fields["owner"].get_default()
        return super().save(**kwargs)


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Membership
        fields = "__all__"
        read_only_fields = ["__all__"]


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
    grade_present = serializers.IntegerField()

    class Meta:
        model = m.CompletedTask
        fields = "__all__"
        read_only_fields = ["owner", "grade_present"]


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

