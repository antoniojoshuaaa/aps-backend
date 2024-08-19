from rest_framework import generics
from .models import Staff, ScopusProfile
from projects.models import Project
from projects.serializers import ProjectSerializer
from .serializers import StaffSerializer
from rest_framework.pagination import PageNumberPagination
from publications.views import GetScopusPublicationByAuthorId
from projects.views import ProjectsByStaffIdView
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 100

class StaffList(generics.ListAPIView):
    serializer_class = StaffSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        value = self.request.query_params.get('searchQuery', '')
        if (value != ''):
            return Staff.objects.filter(staff_name__icontains=value)
        return Staff.objects.all()

class GetStaffById(generics.RetrieveAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    lookup_field = 'staff_id'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        staff = self.get_object()
        data = response.data
        
        projects_data = Project.objects.filter(staff=staff)
        project_serializer = ProjectSerializer(projects_data, many=True)
        if projects_data.first():
            data['projects'] = project_serializer.data
        
        scopusProfile = ScopusProfile.objects.filter(id_owner=staff).first()
        
        if not scopusProfile:
            return Response(data, 200)
        # Correctly call the get_publications method without instantiating the view
        
        publication_view = GetScopusPublicationByAuthorId()
        scopus_data, status_code = publication_view.get_publications(staff)

        data['scopus_publications'] = scopus_data
        data['scopus_profile_link'] = scopusProfile.link

        return Response(data, 200)
