# Create your models here.
from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class CourseScopeModelInterface:
    """Return course instance"""
    def get_associated_course(self):
        """Must be a property"""
        raise NotImplementedError


class OwnedModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, )

    class Meta:
        abstract = True


# class CourseScopeModel(CourseScopeModelInterface, OwnedModel,):     #  INVESTIGATE
#     pass
# training_platform.Comment.grade: (models.E006) The field 'grade' clashes with the field 'grade'
# from model 'training_platform.coursescopemodel'

class Course(CourseScopeModelInterface, OwnedModel, ):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, )

    @property
    def get_associated_course(self):
        return self

    def __str__(self):
        return f"Course {self.id} {self.name}"


class Membership(OwnedModel):
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
    def get_associated_course(self):
        return self.course.get_associated_course

    def __str__(self):
        return f"Lesson {self.id} {self.name}"


class Task(CourseScopeModelInterface, OwnedModel, ):
    content = models.TextField(blank=True, )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="tasks",)

    @property
    def get_associated_course(self):
        return self.lesson.get_associated_course

    def __str__(self):
        return f"Task {self.id}"


class CompletedTask(CourseScopeModelInterface, OwnedModel, ):
    content = models.TextField(blank=True, )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="completed_tasks",)

    @property
    def get_associated_course(self):
        return self.task.get_associated_course

    def __str__(self):
        return f"CompletedTask {self.id}"


class Grade(CourseScopeModelInterface, OwnedModel, ):
    amount = models.IntegerField()
    completed_task = models.OneToOneField(CompletedTask, on_delete=models.CASCADE, related_name="grade",)

    @property
    def get_associated_course(self):
        return self.completed_task.get_associated_course

    def __str__(self):
        return f"Grade {self.id} {self.amount}"


class Comment(CourseScopeModelInterface, OwnedModel, ):
    content = models.TextField(blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="comments", null=True)

    @property
    def get_associated_course(self):
        return self.grade.get_associated_course

    def __str__(self):
        return f"Comment {self.id}"
