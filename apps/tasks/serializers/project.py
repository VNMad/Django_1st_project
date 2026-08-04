from rest_framework import serializers
from apps.tasks.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']

class ProjectInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'