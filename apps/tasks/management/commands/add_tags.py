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
        tag_1 = Tag(name='Backend')
        tag_2 = Tag(name='Frontend')
        tag_3 = Tag(name='Q&A')
        tag_4 = Tag(name='Design')
        tag_5 = Tag(name='DevOPS')
        Tag.objects.bulk_create([tag_1, tag_2, tag_3, tag_4, tag_5])
