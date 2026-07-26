from django.core.management.base import BaseCommand
from apps.tasks.models import Project, Task, Tag, Status, Priorities
from faker import Faker
from django.contrib.auth import get_user_model
import random

User = get_user_model()
fake = Faker()

all_statuses = [choice.value for choice in Status]
all_priorities = [choice.value for choice in Priorities]
all_users = [user for user in User.objects.all()]

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        i = 0
        for project in Project.objects.all():
            for tag in Tag.objects.all():
                task = Task.objects.create(title=fake.word() + str(i),
                                    description=fake.paragraph(nb_sentences=random.randint(2, 5)),
                                    status=random.choice(all_statuses),
                                    priority=random.choice(all_priorities),
                                    project=project,
                                    assignee=random.choice(all_users)
                                    )
                task.tags.add(tag)
                task.save()
                i += 1
