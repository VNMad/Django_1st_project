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
        projects = [Project(name=fake.word(), description=fake.paragraph(nb_sentences=random.randint(2, 5))) for _ in range(10)]
        Project.objects.bulk_create(projects)
        self.stdout.write('Projects created!')