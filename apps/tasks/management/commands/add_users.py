from django.core.management.base import BaseCommand
from apps.tasks.models import Project, Task, Tag, Status, Priorities
from faker import Faker
from django.contrib.auth import get_user_model
import random

User = get_user_model()
fake = Faker()

all_statuses = [choice.value for choice in Status]
all_priorities = [choice.value for choice in Priorities]

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = [User(username='Backend', password='12345'),
                 User(username='Frontend', password='12345'),
                 User(username='DevOPS', password='12345'),
                 User(username='Q&A', password='12345'),
                 User(username='Designer', password='12345')]
        User.objects.bulk_create(users)
