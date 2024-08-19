from requests import Response
from rest_framework import generics
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 100

class ProjectsByStaffIdView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    
    def list(self, staff):
        projects = Project.objects.filter(su_staff=staff)
        serializer = ProjectSerializer(projects, many=True)
        if projects:
            return serializer.data, 200
        return [], 404

class ProjectsListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        searchQuery = self.request.query_params.get('search_query')
        if not searchQuery:
            return Project.objects.all()
        
        return Project.objects.filter(project_title__icontains=searchQuery)

class ProjectByProjectIdView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    lookup_field = 'project_code'
    serializer_class = ProjectSerializer

