from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory
from factory import LazyAttribute, SelfAttribute
from training_platform import models as m


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")

    # name = Faker("name")
    # password = LazyAttribute(lambda o: o.username)

    # password = SelfAttribute("username")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else self.username
            # else Faker(
            #     "password",
            #     length=42,
            #     special_chars=True,
            #     digits=True,
            #     upper_case=True,
            #     lower_case=True,
            # ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class CourseFactory(DjangoModelFactory):
    name = Faker("word")
    description = Faker("paragraph")

    class Meta:
        model = m.Course
        django_get_or_create = ["name"]


class MembershipFactory(DjangoModelFactory):
    class Meta:
        model = m.Membership
        django_get_or_create = ["user", "course"]


class LessonFactory(DjangoModelFactory):
    name = Faker("word")
    content = Faker("paragraph")

    class Meta:
        model = m.Lesson
        django_get_or_create = ["name", "course"]


class TaskFactory(DjangoModelFactory):
    content = Faker("paragraph")

    class Meta:
        model = m.Task
        django_get_or_create = ["lesson", "course", "content"]


class CompletedTaskFactory(DjangoModelFactory):
    content = Faker("paragraph")

    class Meta:
        model = m.CompletedTask
        django_get_or_create = ["task", "course", "content"]


class GradeFactory(DjangoModelFactory):
    amount = Faker("random_int", min=0, max=100)

    class Meta:
        model = m.Grade
        django_get_or_create = ["completed_task", "course"]


class CommentFactory(DjangoModelFactory):
    content = Faker("sentence")

    class Meta:
        model = m.Comment
        django_get_or_create = ["grade", "course", "content"]
