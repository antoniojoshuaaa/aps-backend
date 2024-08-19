from rest_framework import serializers
from .models import Project, Sponsor
from db.serializers import StaffSerializer

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['sponsor_name']
        
class ProjectSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True, many=False)
    sponsor = SponsorSerializer(read_only=True)
    class Meta:
        model = Project
        fields = ["project_code", "project_title", "grant_name", "sponsor", "staff", "project_start_date", "project_end_date", "collaborators", "amount_awarded"]

        