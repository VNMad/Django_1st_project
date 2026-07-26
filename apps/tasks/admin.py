from django.conf import settings
from django.contrib import admin
from .models import Category, Task, SubTask, Project, Tag, ProjectFile, Status, Priorities
from django.db.models import F, Value
from django.db.models.functions import Replace


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'show_files_quantity')
    search_fields = ('name',)

    @admin.display(description='Files quantity')
    def show_files_quantity(self, projects):
        return projects.files.count()

    @admin.action(description='Replace all spaces to _ symbol')
    def replace_space_to__(self, request, projects):
        # for project in projects:
        #     project.name = project.name.replace(' ', '_')
        # projects.bulk_update(projects, ['name'])
        projects.update(name=Replace('name', Value('s'), Value('E')))

    actions = [replace_space_to__]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]
    ordering = ["name"]
    fields = ["name"]
    list_per_page = 10


class SubTaskInline(admin.StackedInline):
    model = SubTask
    extra = 1
    show_change_link = True


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("short_title", "get_categories", "status", "deadline", "created_at", "description")
    list_filter = ("status", "categories")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    fields = ("title", "categories", "status", "deadline", "description")
    list_per_page = 10

    inlines = [SubTaskInline]

    @admin.display(description="Title")
    def short_title(self, obj):
        return f"{obj.title[:10]}..." if len(obj.title) > 10 else obj.title

    @admin.display(description="Categories")
    def get_categories(self, obj):
        return ", ".join(category.name for category in obj.categories.all())

    @admin.action(description='Replace specific status to DONE')
    def replace_status_to_done(self, request, tasks):
        tasks.update(status=Status.DONE)
    actions = [replace_status_to_done]


    priorities = [(priority.value, priority.name) for priority in Priorities]
    for key, value in priorities:
        add_priority = lambda self, request, tasks, p=key: tasks.update(priority=p)
        add_priority.__name__ = key
        add_priority.short_description = f'Change specific priority to {value}'
        actions.append(add_priority)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "status", "deadline", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    fields = ("task", "title", "description", "status", "deadline")
    list_per_page = 10


    @admin.action(description="Change status to Done")
    def replace_status_to_done(self, request, subtasks):
        subtasks.update(status=Status.DONE)

    actions = [replace_status_to_done]