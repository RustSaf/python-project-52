from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import Users
from task_manager.users.views import (
    IndexView,
    UserCreateView,
    UserDeleteView,
    UserUpdateView,
)

# Create your tests here.
