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
        user_1 = User.objects.first()
        project_1 = Project.objects.create(name=fake.first_name(),
                                           description=fake.paragraph(nb_sentences=random.randint(2, 5)))
        Task.objects.create(name=fake.first_name(),
                            description=fake.paragraph(nb_sentences=random.randint(2, 5)),
                            status=random.choice(all_statuses),
                            priority=random.choice(all_priorities),
                            project=project_1,
                            assignee=user_1,
                            )

