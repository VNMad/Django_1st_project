from django.core.management.base import BaseCommand
from apps.tasks.models import Project, Task, Tag, Status, Priorities, ProjectFile
from faker import Faker
from django.contrib.auth import get_user_model
import random
from django.core.files.base import ContentFile

User = get_user_model()
fake = Faker()

all_statuses = [choice.value for choice in Status]
all_priorities = [choice.value for choice in Priorities]

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for project in Project.objects.all():
            for i in range(random.randint(3, 5)):
                our_file = ProjectFile(name=f'file_{i}.txt')
                our_file.file.save(f'file_{i}.txt',
                    ContentFile(fake.paragraph(nb_sentences=random.randint(2, 5))), save=True)
                our_file.save()
                project.files.add(our_file)
                project.save()