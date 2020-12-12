# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class CourseScopeModelInterface:
    """Return course instance"""
    def courseroot(self):
        """Must be a property"""
        raise NotImplementedError


class User(AbstractUser):
    is_teacher = models.BooleanField('teacher status', default=False)


class OwnedModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, )

    class Meta:
        abstract = True


class Course(CourseScopeModelInterface, OwnedModel, ):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, )

    @property
    def courseroot(self):
        return self

    def __str__(self):
        return f"Course {self.id} {self.name}"


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="memberships")

    def __str__(self):
        return f"Membership U {self.user} C {self.course}"


class Lesson(CourseScopeModelInterface, OwnedModel, ):
    name = models.CharField(max_length=150)
    content = models.TextField(blank=True, )
    file = models.FileField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons",)

    @property
    def courseroot(self):
        return self.course.courseroot

    def __str__(self):
        return f"Lesson {self.id} {self.name}"


class Task(CourseScopeModelInterface, OwnedModel, ):
    content = models.TextField(blank=True, )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="tasks",)

    @property
    def courseroot(self):
        return self.lesson.courseroot

    def __str__(self):
        return f"Task {self.id}"


class CompletedTask(CourseScopeModelInterface, OwnedModel, ):
    content = models.TextField(blank=True, )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="completed_tasks",)

    @property
    def courseroot(self):
        return self.task.courseroot

    def __str__(self):
        return f"CompletedTask {self.id}"


class Grade(CourseScopeModelInterface, OwnedModel, ):
    amount = models.IntegerField()
    completed_task = models.OneToOneField(CompletedTask, on_delete=models.CASCADE, related_name="grade",)

    @property
    def courseroot(self):
        return self.completed_task.courseroot

    def __str__(self):
        return f"Grade {self.id} {self.amount}"


class Comment(CourseScopeModelInterface, OwnedModel, ):
    content = models.TextField(blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="comments", null=True)

    @property
    def courseroot(self):
        return self.grade.courseroot

    def __str__(self):
        return f"Comment {self.id}"

