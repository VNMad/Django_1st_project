from django.core.management.base import BaseCommand
from apps.tasks.models import Project, Task, Tag, Status, Priorities
from faker import Faker
from django.contrib.auth import get_user_model
import random
from django.db.models import F, Q

User = get_user_model()
fake = Faker()

all_tags = {'Backend': 'Добавить новый эндпоинт',
            'Frontend': 'Обновить страницу ответа 404',
            'DevOPS': 'Настройка CI/CD, после сконфигурировать Docker',
            'Q&A': 'Написание автотестов',
            'Designer': 'Разработка UI-кита и редизайн макета'}

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        all_users = [user.username for user in User.objects.all()]
        for task in Task.objects.all():
            tag_name = all_tags.get(task.assignee.username if task.assignee else random.choice(all_users))
            if not tag_name:
                tag_name = 'Common task'
            matched_tag, _ = Tag.objects.get_or_create(name=tag_name)
            task.tags.add(matched_tag)
            print(task.title, task.tags)
        self.stdout.write('Tags assigned!')


        # for task in Task.objects.all():
        #     for user in User.objects.all():
        #         if user.username == 'Backend':
        #             task.tags.add(Tag(name='Добавить новый эндпоинт'))
        #         elif user.username == 'Frontend':
        #             task.tags.add(Tag(name='Обновить страницу ответа 404'))
        #         elif user.username == 'DevOPS':
        #             task.tags.add(Tag(name='Обновить страницу ответа 404'))
        #         elif user.username == 'Q&A':
        #             task.tags.add(Tag(name='Обновить страницу ответа 404'))
        #         elif user.username == 'Designer':
        #             task.tags.add(Tag(name='Обновить страницу ответа 404'))

