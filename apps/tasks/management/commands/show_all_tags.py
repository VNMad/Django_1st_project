from django.core.management.base import BaseCommand
from apps.tasks.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        all_tags = Tag.objects.all()
        print(*(f'Tag: {tag.name}' for tag in all_tags), sep='\n')
        print(f'Most first tag: {Tag.objects.first()}')
        print(f'Last tag: {Tag.objects.last()}')
        print(f'Tags count: {Tag.objects.count()}')