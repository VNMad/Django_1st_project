from rest_framework import serializers
from apps.tasks.models import Task
from .tags import TagSerializer
from .categories import CategorySerializer


class TaskInfoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    categories = CategorySerializer(many=True)
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "deadline",
            "project",
            "assignee",
            "categories",
            "tags",
            "created_at",
            "updated_at",
        ]
