import os

import django

from datetime import timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.tasks.models import Task, Category, SubTask, Status


def create_objects():
    task = Task(
        title="Prepare presentation",
        description="Prepare materials and slides for the presentation",
        status=Status.NEW,
        deadline=timezone.now() + timedelta(days=3),
    )

    print(task.id)
    print(task.title)

    task.save()
    category = Category.objects.get(name="Work")
    task.categories.add(category)

def create_subtasks():
    task = Task.objects.get(title="Prepare presentation")

    subtask = SubTask.objects.create(
        title="Gather information",
        description="Find necessary information for the presentation",
        task=task,
        status=Status.NEW,
        deadline=timezone.now() + timedelta(days=2),
    )

    print(subtask.id)
    print(subtask.title)

    subtask = SubTask.objects.create(
        title="Create slides",
        description="Create presentation slides",
        task=task,
        status=Status.NEW,
        deadline=timezone.now() + timedelta(days=1),
    )

    print(subtask.id)
    print(subtask.title)

def get_objects():
    tasks = Task.objects.filter(status=Status.NEW)
    for task in tasks:
        print(f'{task.status} - {task.title}')

    subtasks = SubTask.objects.filter(status=Status.DONE, deadline__lt=timezone.now())
    for subtask in subtasks:
        print(f'{subtask.status} - {subtask.title}')


def update_objects():

    task = Task.objects.get(title="Prepare presentation")
    print(f'{task.status} - {task.title}')
    task.status = Status.IN_PROGRESS
    task.save()
    print(f'{task.status} - {task.title}')

    subtask = SubTask.objects.get(title="Gather information")
    print(f'{subtask.deadline} - {subtask.title}')
    subtask.deadline = timezone.now() - timedelta(days=2)
    subtask.save()
    print(f'{subtask.deadline} - {subtask.title}')

    subtask = SubTask.objects.get(title="Create slides")
    print(f'{subtask.title} - {subtask.description}')
    SubTask.objects.filter(title="Create slides").update(description="Create and format presentation slides")
    subtask = SubTask.objects.get(title="Create slides")
    print(f'{subtask.title} - {subtask.description}')


def delete_objects():
    tasks = Task.objects.filter(title="Prepare presentation")

    for task in tasks:
        print(f'Deleted task: {task.title}')
        for subtask in task.subtasks.all():
            print(f"  SubTask: {subtask.title}")

    count, details = tasks.delete()

    print(f"\nDeleted objects: {count}")
    print(details)

if __name__ == "__main__":
    #create_objects()
    #create_subtasks()
    #get_objects()
    #update_objects()
    delete_objects()