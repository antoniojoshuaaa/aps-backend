from db.models import Staff, ScopusProfile
from projects.models import Project

def run():
    # staffs = Staff.objects.all()
    # projects = Project.objects.all()

    # for project in projects:
    #     new_code = project.project_code.replace("/", "-")
    #     project.project_code = new_code
    #     print(f"Old code: {project.project_code} -> New code: {new_code}")
        
    #     try:
    #         project.save()
    #         print(f"Project {project.id} saved successfully with new code: {project.project_code}")
    #     except Exception as e:
    #         print(f"Error saving project {project.id}: {e}")
    print(Project.objects.all())