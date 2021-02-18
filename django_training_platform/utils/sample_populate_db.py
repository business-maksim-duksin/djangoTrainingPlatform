from training_platform.models import *
from django.contrib.auth import get_user_model
from . import factories as f



def sample_populate_db():
    student_1 = f.UserFactory(username='s1', is_teacher=False)
    student_2 = f.UserFactory(username='s2', is_teacher=False)
    student_3 = f.UserFactory(username='s3', is_teacher=False)

    teacher_math = f.UserFactory(username='t_math', is_teacher=True)
    teacher_stat = f.UserFactory(username='t_stat', is_teacher=True)

# MATH COURSE
# ------------------------------------------------------------------------------
    course_math = f.CourseFactory(name='math', owner=teacher_math)

    f.MembershipFactory(owner=teacher_math, course=course_math, user=teacher_math)
    f.MembershipFactory(owner=teacher_math, course=course_math, user=teacher_stat)
    f.MembershipFactory(owner=teacher_math, course=course_math, user=student_1)
    f.MembershipFactory(owner=teacher_math, course=course_math, user=student_2)
    f.MembershipFactory(owner=teacher_math, course=course_math, user=student_3)

    l1 = f.LessonFactory(owner=teacher_math, course=course_math, name="math_1")
    l2 = f.LessonFactory(owner=teacher_math, course=course_math, name="math_2")

    t1 = f.TaskFactory(owner=teacher_math, course=course_math, lesson=l1,)
    t2 = f.TaskFactory(owner=teacher_math, course=course_math, lesson=l1,)
    t3 = f.TaskFactory(owner=teacher_stat, course=course_math, lesson=l2, )

    ct1_1 = f.CompletedTaskFactory(owner=student_1, course=course_math, task=t1)
    gr1 = f.GradeFactory(owner=teacher_math, course=course_math, completed_task=ct1_1)
    com1 = f.CommentFactory(owner=teacher_math, course=course_math, grade=gr1)
    com2 = f.CommentFactory(owner=student_1, course=course_math, grade=gr1)
    com3 = f.CommentFactory(owner=teacher_math, course=course_math, grade=gr1)
    gr2 = f.GradeFactory(owner=teacher_math, course=course_math, completed_task=ct1_1)

    ct1_2 = f.CompletedTaskFactory(owner=student_1, course=course_math, task=t1)

    ct1_3 = f.CompletedTaskFactory(owner=student_2, course=course_math, task=t1)
    gr2 = f.GradeFactory(owner=teacher_math, course=course_math, completed_task=ct1_3)

    ct1_4 = f.CompletedTaskFactory(owner=student_3, course=course_math, task=t1)
    gr3 = f.GradeFactory(owner=teacher_math, course=course_math, completed_task=ct1_4)

    ct2_1 = f.CompletedTaskFactory(owner=student_1, course=course_math, task=t2)
    ct2_2 = f.CompletedTaskFactory(owner=student_2, course=course_math, task=t2)
    ct2_3 = f.CompletedTaskFactory(owner=student_3, course=course_math, task=t2)
    ct3_1 = f.CompletedTaskFactory(owner=student_2, course=course_math, task=t3)
    gr4 = f.GradeFactory(owner=teacher_math, course=course_math, completed_task=ct3_1)
    ct3_2 = f.CompletedTaskFactory(owner=student_3, course=course_math, task=t3)
    gr5 = f.GradeFactory(owner=teacher_stat, course=course_math, completed_task=ct3_2)










