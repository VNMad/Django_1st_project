from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
import uuid


class UniqueId(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='UUID id')

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Status(models.TextChoices):
    NEW = "new", "New"
    IN_PROGRESS = "in_progress", "In progress"
    PENDING = "pending", "Pending"
    BLOCKED = "blocked", "Blocked"
    DONE = "done", "Done"


class Category(UniqueId):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(3)], unique=True, verbose_name='Category name')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Task(UniqueId, TimeStampedModel):
    title = models.CharField(max_length=100, validators=[MinLengthValidator(3)], unique=True, verbose_name='Title')
    description = models.TextField(validators=[MinLengthValidator(3)], verbose_name='Description')
    categories = models.ManyToManyField(Category, related_name='tasks')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW, verbose_name='Status')
    deadline = models.DateTimeField(verbose_name='Deadline')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class SubTask(UniqueId, TimeStampedModel):
    title = models.CharField(max_length=100, validators=[MinLengthValidator(3)], unique=True, verbose_name='Title')
    description = models.TextField(validators=[MinLengthValidator(3)], verbose_name='Description')
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW, verbose_name='Status')
    deadline = models.DateTimeField(verbose_name='Deadline')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = _('SubTask')
        verbose_name_plural = _('SubTasks')