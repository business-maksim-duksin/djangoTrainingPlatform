from training_platform.models import *
from django.contrib.auth import get_user_model
from factories import UserFactory



def sample_populate_db():
    user = UserFactory(username="s1", is_teacher=False)
    pass