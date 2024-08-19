from django.db import models
from django.utils.translation import gettext_lazy as _
from db.models import Staff

class Sponsor(models.Model):
    class Category(models.TextChoices):
        INTERNATIONAL = "International", _("International")
        NATIONAL = "National", _("National")
        COLLABORATION = "Collaboration", _("Collaboration")
        PRIVATE = "Private", _("Private")

    sponsor_id = models.CharField(max_length=20, primary_key=True)
    sponsor_name = models.CharField(max_length=256, unique=True)
    sponsor_category = models.CharField(max_length=20, choices=Category.choices, default=Category.NATIONAL)

    def __str__(self):
        return self.sponsor_name


class Project(models.Model):
    project_code = models.CharField(max_length=256, primary_key=True)
    project_title = models.CharField(max_length=256)
    grant_name = models.TextField(null=True, blank=True)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, db_column='sponsor_name', null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, db_column='staff_id', null=True, blank=True)
    project_start_date = models.DateField(max_length=256, blank=True, null=True)
    project_end_date = models.DateField(max_length=256, blank=True, null=True)
    collaborators = models.TextField(blank=True, null=True, default=None)
    amount_awarded = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.project_title} ({self.staff.staff_name})" 
        
