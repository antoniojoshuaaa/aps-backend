import pandas as pd
from db.models import Staff
from projects.models import Sponsor, Project
from decimal import Decimal

def run():
    # Read the CSV file with pandas
    csv_file_path = 'projects/grants.csv'
    data = pd.read_csv(csv_file_path, encoding='utf-8')
    
    # Clear existing data
    Sponsor.objects.all().delete()
    Project.objects.all().delete()
    
    for index, row in data.iterrows():
        sponsor_name = row['SPONSOR']
        sponsor_category = row['SPONSOR CATEGORY']
        grant_name = row['GRANT NAME']
        project_title = row['PROJECT TITLE']
        staff_name = row['SU STAFF']
        start_date = row['Project Start Date']
        end_date = row['Project End Date']
        amount_awarded = row['AMOUNT AWARDED']
        collaborators = row['COLLABORATORS']
        
        # Check if a Staff record with the same staff_name exists
        existing_staff = Staff.objects.filter(staff_name__iexact=staff_name).first()
        if existing_staff:
            # Create or get Sponsor instance
            sponsor, created = Sponsor.objects.get_or_create(
                sponsor_name=sponsor_name,
                sponsor_category=sponsor_category,
                defaults={'sponsor_id': f"{sponsor_name[:3].upper()}{Sponsor.objects.count() + 1:04d}"}
            )
            
            # Clean and convert amount_awarded to Decimal
            amount_awarded = amount_awarded.strip().replace(',', '')
            if amount_awarded:
                amount_awarded = Decimal(amount_awarded)
            else:
                amount_awarded = None
            
            # Generate a unique project code
            project_code = f"{sponsor_name[:3].upper()}{index + 1:04d}"
            
            # Create or get Project instance
            project, created = Project.objects.get_or_create(
                project_code=project_code,
                defaults={
                    'project_title': project_title,
                    'grant_name': grant_name,
                    'sponsor': sponsor,
                    'staff': existing_staff,
                    'project_start_date': pd.to_datetime(start_date).date() if pd.notna(start_date) else None,
                    'project_end_date': pd.to_datetime(end_date).date() if pd.notna(end_date) else None,
                    'amount_awarded': amount_awarded,
                    'collaborators': collaborators,
                }
            )
            
            if created:
                print(f"Added grant {grant_name} for staff {existing_staff.staff_name}")
            else:
                print(f"Grant {grant_name} for staff {existing_staff.staff_name} already exists.")
            
            # Save the Project instance
            project.save()
        else:
            print(f"Staff {staff_name} doesn't exist in the system.")
