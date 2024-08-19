# Import Django settings correctly
import os
import requests
from django.conf import settings
from db.models import Staff, ScopusProfile  # Adjust import path based on your project structure
import logging

# Load Scopus API key from Django settings
SCOPUS_API_KEY = settings.SCOPUS_API_KEY

def run():
    all_staff = Staff.objects.all()
    ScopusProfile.objects.all().delete()

    headers = {
        'Accept': 'application/json',
        'X-ELS-APIKey': SCOPUS_API_KEY,
    }

    for staff in all_staff:
        names = staff.staff_name.split()
        if len(names) >= 2:
            first_name = ' '.join(names[:-1])  # Join first names with spaces
            last_name = names[-1]  # Last name is the last element

            # Form the payload with the formatted query
            payload = {
                'query': f'AUTHLAST({last_name}) AND AUTHFIRST({first_name}) AND af-id(60107208)',
            }

            # Make the API request
            r = requests.get('https://api.elsevier.com/content/search/author', headers=headers, params=payload)
            json_response = r.json()

            # Process the JSON response
            if 'search-results' in json_response and 'entry' in json_response['search-results']:
                for entry in json_response['search-results']['entry']:
                    if 'error' in entry:
                        # Handle error case, you can log the error message
                        logging.error(f"Error for {staff.staff_name}: {entry['error']}")
                        continue  # Skip to the next entry if there's an error
                    
                    author_id = entry.get('dc:identifier', '').replace('AUTHOR_ID:', '')
                    newScopusId = ScopusProfile.objects.create(
                        scopus_author_id = author_id,
                        id_owner = staff,
                        link = entry['link'][3]['@href']
                    )
                    print(f"Author ID for {staff.staff_name}: {newScopusId.scopus_author_id}")
                    print(f"Link: {newScopusId.link}")
                    staff.scopus_author_id = author_id
                    staff.save()
            # Optionally, you may want to save this data back to your Staff model or do other processing

if __name__ == "__main__":
    run()