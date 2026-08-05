from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views as projects_


urlpatterns = [
    path('projects/', projects_.get_all_projects),
    path('projects/<uuid:pk>', projects_.get_project_by_id),
    path('tasks/', projects_.put_or_get_all_tasks),
    path('tasks/<uuid:pk>', projects_.get_task_by_id),
    path("tasks/statistics/", projects_.task_statistics),
    path('tags/', projects_.post_or_show_all_tags),
    path('tags/<uuid:pk>', projects_.get_or_upd_tag_by_id)
]