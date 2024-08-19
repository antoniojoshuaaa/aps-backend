from django.db import models
from django.utils.translation import gettext_lazy as _
import os
from django.core.exceptions import SuspiciousFileOperation
from django.utils._os import safe_join

def upload_to(instance, filename):
    filename = os.path.basename(filename)
    if '..' in filename or filename.startswith('/'):
        raise SuspiciousFileOperation(f"Detected path traversal attempt in '{filename}'")
    return safe_join('media/profile', filename)

class Staff(models.Model):
    staff_id = models.CharField(primary_key=True, max_length=10)
    staff_name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(_("Image"), default='/profile_placeholder.jpg', upload_to=upload_to)
    title = models.CharField(max_length=255, null=True, blank=True)    
    department = models.CharField(max_length=255, default=None, null=True, blank=True)
    school = models.CharField(max_length=255, default=None, null=True, blank=True)
    email = models.EmailField(max_length=255, default="example@sunway.edu.my")
    biography = models.TextField(blank=True, default="")
    research_interests = models.CharField(max_length=255, default="", blank=True)
    def __str__(self):
        return self.staff_name

class ScopusProfile(models.Model):
    scopus_author_id = models.CharField(max_length=255, default=None, primary_key=True)
    id_owner = models.ForeignKey(Staff, on_delete=models.CASCADE)
    link = models.TextField(default=None, null=True, blank=True)
    
    def __str__(self):
        return self.id_owner.staff_name + f" ({self.scopus_author_id})"
