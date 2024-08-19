from django.urls import path, include
from .views import ProjectsByStaffIdView, ProjectsListView, ProjectByProjectIdView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('', ProjectsListView.as_view(), name="project-list-view"),
    path('staff_id/<str:staff_id>/', ProjectsByStaffIdView.as_view(), name="project-by-staff-id-view"),
    path('project_code/<str:project_code>/', ProjectByProjectIdView.as_view(), name="project-by-project-code-view"),
]
