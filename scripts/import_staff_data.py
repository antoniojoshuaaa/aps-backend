import csv
from db.models import Staff

def run():
    with open('db/staff-data.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header
        
        for row in reader:
            title = row[1]
            staff_id = row[2]
            staff_name = row[3]
            department = row[4]
            school = row[5]
            
            # Check if a Staff record with the same staff_id exists
            existing_staff = Staff.objects.filter(staff_name=staff_name).first()
            
            if existing_staff:
                # If a record with the same staff_id exists, update the fields
                existing_staff.title = title
                existing_staff.staff_name = staff_name
                existing_staff.department = department
                existing_staff.school = school
                existing_staff.save()
                print(f"Updated profile for {staff_name}")
            else:
                # If no record with the same staff_id exists, create a new Staff object
                Staff.objects.create(
                    title=title,
                    staff_id=staff_id,
                    staff_name=staff_name,
                    department=department,
                    school=school
                )
                print(f"Created profile for {staff_name}")

if __name__ == "__main__":
    run()
