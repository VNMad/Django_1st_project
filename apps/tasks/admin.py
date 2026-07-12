from django.contrib import admin
from .models import Category, Task, SubTask


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "get_categories", "status", "deadline", "created_at", "description")
    list_filter = ("status", "categories")
    search_fields = ("title", "description")
    @admin.display(description="Categories")
    def get_categories(self, obj):
        return ", ".join(category.name for category in obj.categories.all())

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "status", "deadline", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "description")