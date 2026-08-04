from rest_framework import serializers
from apps.tasks.models import Task
from .tags import TagSerializer
from .categories import CategorySerializer


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "deadline",
        ]

class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    categories = CategorySerializer(many=True)
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'project',
            'categories',
            'tags',
        ]