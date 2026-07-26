from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
import uuid
from django.conf import settings


class UniqueId(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='UUID id')

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Status(models.TextChoices):
    NEW = 'new', _('New')
    IN_PROGRESS = 'in_progress', _('In progress')
    PENDING = 'pending', _('Pending')
    BLOCKED = 'blocked', _('Blocked')
    DONE = 'done', _('Done')
    CLOSED = 'closed', _('Closed')


class Priorities(models.TextChoices):
    LOW = 'l', _('Low')
    MEDIUM = 'm', _('Medium')
    HIGH = 'h', _('High')
    URGENT = 'u', _('Urgent')
    CRITICAL = 'c', _('Critical')


class Category(UniqueId):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(3)], unique=True, verbose_name='Category name')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Project(UniqueId, TimeStampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Project's name")
    description = models.TextField(verbose_name='Description')
    files = models.ManyToManyField('ProjectFile', related_name='projects', verbose_name='Files')

    def __str__(self):
        return f'Project: {self.name}'

    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ('-name',)
        unique_together = (('name', 'description'),)


class Task(UniqueId, TimeStampedModel):
    title = models.CharField(max_length=100, validators=[MinLengthValidator(3)], unique=True, verbose_name='Title')
    description = models.TextField(validators=[MinLengthValidator(3)], verbose_name='Description')
    categories = models.ManyToManyField(Category, related_name='tasks')
    status = models.CharField(max_length=20, choices=Status, default=Status.NEW, verbose_name='Status')
    priority = models.CharField(max_length=15, choices=Priorities, verbose_name='Priority')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name='Project')
    deadline = models.DateTimeField(verbose_name='Deadline')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks', verbose_name='Assignees', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='tasks', verbose_name='Tags')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        unique_together = ('title', 'project')


class SubTask(UniqueId, TimeStampedModel):
    title = models.CharField(max_length=100, validators=[MinLengthValidator(3)], unique=True, verbose_name='Title')
    description = models.TextField(validators=[MinLengthValidator(3)], verbose_name='Description')
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status, default=Status.NEW, verbose_name='Status')
    deadline = models.DateTimeField(verbose_name='Deadline')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = _('SubTask')
        verbose_name_plural = _('SubTasks')


class Tag(UniqueId, TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'Tag: {self.name}'

    def __repr__(self):
        return f'<Tag(name={self.name})>'



class ProjectFile(UniqueId, TimeStampedModel):
    name = models.CharField(max_length=120, verbose_name='File name')
    file = models.FileField(upload_to='projects/')

    def __str__(self):
        return f'ProjectFile: name {self.name}, path {self.file}'

    class Meta:
        db_table = 'project_files'
        verbose_name = 'ProjectFile'
        verbose_name_plural = 'ProjectFiles'
        ordering = ('-created_at',)