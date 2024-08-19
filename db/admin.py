from django.contrib import admin
from django.contrib.auth.models import Group
from db.models import Staff, ScopusProfile
from projects.models import Project, Sponsor

admin.site.unregister(Group)

class ScopusProfileInline(admin.StackedInline):
    model = ScopusProfile
    can_delete = True
    verbose_name_plural = 'Scopus Profiles'

class StaffAdmin(admin.ModelAdmin):
    list_display = ("staff_id", "staff_name", "title", "department", "school", "email", "biography", "research_interests")
    search_fields = ("staff_id", "staff_name", "department", "school")
    inlines = [ScopusProfileInline]

admin.site.register(Staff, StaffAdmin)

class ScopusProfileAdmin(admin.ModelAdmin):
    list_display = ("scopus_author_id", "id_owner", "link")
    search_fields = ("id_owner__staff_name", "scopus_author_id")

admin.site.register(ScopusProfile, ScopusProfileAdmin)

admin.site.register(Project)
admin.site.register(Sponsor)
