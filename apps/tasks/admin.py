from django.contrib import admin
from .models import Category, Task, SubTask


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]
    ordering = ["name"]
    fields = ["name"]
    list_per_page = 10


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "get_categories", "status", "deadline", "created_at", "description")
    list_filter = ("status", "categories")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    fields = ("title", "categories", "status", "deadline", "description")
    list_per_page = 10

    @admin.display(description="Categories")
    def get_categories(self, obj):
        return ", ".join(category.name for category in obj.categories.all())


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "status", "deadline", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    fields = ("task", "title", "description", "status", "deadline")
    list_per_page = 10