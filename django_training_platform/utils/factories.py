from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory
from factory import LazyAttribute, SelfAttribute
from training_platform import models as m


class UserFactory(DjangoModelFactory):

    # username = Faker("user_name")
    # email = Faker("email")
    # name = Faker("name")
    # password = LazyAttribute(lambda o: o.username)
    password = SelfAttribute("username")

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class CourseFactory(DjangoModelFactory):

    class Meta:
        model = m.Course
        django_get_or_create = ["id"]


class MembershipFactory(DjangoModelFactory):

    class Meta:
        model = m.Membership
        django_get_or_create = ["user", "course"]


class LessonFactory(DjangoModelFactory):

    class Meta:
        model = m.Lesson
        django_get_or_create = ["id"]


class TaskFactory(DjangoModelFactory):

    class Meta:
        model = m.Lesson
        django_get_or_create = ["id"]