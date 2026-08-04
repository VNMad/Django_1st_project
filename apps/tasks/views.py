from rest_framework import status
from apps.tasks.serializers import ProjectSerializer,  ProjectInfoSerializer, TaskSerializer, TagSerializer, TaskInfoSerializer, TaskCreateSerializer
from rest_framework.decorators import api_view
from apps.tasks.models import Project, Task, Tag, Priorities
#from django.http import JsonResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone


# ---------------- PROJECTS ---------------- #
@api_view(['GET'])
def get_all_projects(request):
    project_name = request.query_params.get('name')
    all_projects = Project.objects.all()
    if project_name:
        all_projects = all_projects.filter(name=project_name)
    serialize_data = ProjectSerializer(all_projects, many=True)
    return Response(data=serialize_data.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_project_by_id(request, pk):
    # try:
    #     project = Project.objects.get(id=pk)
    #     serialize = ProjectSerializer(project)
    #     return Response(data=serialize.data, status=status.HTTP_200_OK)
    # except Project.DoesNotExist:
    #     return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    project = get_object_or_404(Project, id=pk)
    serializer = ProjectInfoSerializer(project)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------- TASKS ---------------- #

@api_view(['POST'])
def create_task(request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(assignee=request.user, project=Project.objects.first(), priority=Priorities.LOW)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_tasks(request):
    specific_project = request.query_params.get('project')
    all_tasks = Task.objects.all()
    if specific_project:
        all_tasks = all_tasks.filter(project__name__icontains=specific_project)
    serializer = TaskSerializer(all_tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_task_by_id(request, pk):
    task_by_id = get_object_or_404(Task, id=pk)
    serializer = TaskInfoSerializer(task_by_id)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------- STATISTICS ---------------- #
@api_view(["GET"])
def task_statistics(request):
    total_tasks = Task.objects.count()
    overdue_tasks = Task.objects.filter(deadline__lt=timezone.now()).count()
    status_statistics = Task.objects.values("status").annotate(count=Count("id"))

    return Response({
        "total_tasks": total_tasks,
        "overdue_tasks": overdue_tasks,
        "status_statistics": status_statistics,
    })


# ---------------- TAGS ---------------- #
@api_view(['GET', 'POST'])
def post_or_show_all_tags(request):
    if request.method == 'GET':
        all_tags = Tag.objects.all()
        serializer = TagSerializer(all_tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': f"New Tag '{serializer.data['name']}' has been created :)"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def get_or_upd_tag_by_id(request, pk):
    tag_by_id = get_object_or_404(Tag, id=pk)
    if request.method == 'GET':
        serializer = TagSerializer(tag_by_id)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        tag_by_id.delete()
        return Response({'msg': f"Tag {pk} has been successfully deleted :)"}, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = TagSerializer(tag_by_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': f"Tag {serializer.data['name']} ({pk}) has been successfully updated :)"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
