from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from db.models import Staff, ScopusProfile
import requests
from core.settings import SCOPUS_API_KEY
from datetime import date
import numpy as np
from urllib.parse import quote
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60*15), name='dispatch')
class GetScopusPublicationByAffiliation(APIView):
    def get(self, request):
        items_per_page = self.request.query_params.get('limit')
        search_query = self.request.query_params.get('search_query')
        curr_page = self.request.query_params.get('page')
        starting_index = int(items_per_page) * (int(curr_page)-1)
        headers = {
            'Accept': 'application/json',
            'X-ELS-APIKey': SCOPUS_API_KEY,
        }
        if search_query != None:
            payload = {
                'query': f"af-id(60107208) AND SRCTITLE({search_query}) OR AUTHKEY({search_query})",
                'view': 'complete',
                'suppressNavLinks': True,   
                'start': starting_index,
                'count': items_per_page,
            }
        else:
            payload = {
                'query': 'af-id(60107208)',
                'view': 'complete',
                'suppressNavLinks': True,
                'start': starting_index,
                'count': items_per_page,
            }
        r = requests.get('https://api.elsevier.com/content/search/scopus', headers=headers, params=payload)
        json = r.json()
        return Response(json)
    
@method_decorator(cache_page(60*15), name='dispatch')
class GetScopusPublicationByAuthorId(APIView):
    def get_publications(self, staff):
        scopus_ids = ScopusProfile.objects.filter(id_owner=staff)

        headers = {
            'Accept': 'application/json',
            'X-ELS-APIKey': SCOPUS_API_KEY,
        }

        payload = {
            'query': '',
            'view': 'complete',
            'suppressNavLinks': True,
        }

        query_parts = []
        for scopus_id in scopus_ids:
            query_parts.append(f"au-id({scopus_id.scopus_author_id})")

        payload['query'] = ' OR '.join(query_parts)
        response = requests.get('https://api.elsevier.com/content/search/scopus', headers=headers, params=payload)
        
        if response.status_code != 200:
            return None, response.status_code

        scopus_data = response.json()
        
        # Sort publications by date (prism:coverDisplayDate)
        publications = scopus_data.get('search-results', {}).get('entry', [])
        scopus_data['search-results']['entry'] = publications

        return scopus_data, response.status_code
    
    def get(self, request):
        staff_id = self.request.query_params.get('staff_id')  # Fetch 'staff_id' from query parameters
        staff = Staff.objects.filter(staff_id=staff_id).first()  # Query Staff model for staff_id
        
        if not staff:
            return Response({'error': 'Staff not found'}, status=404)

        scopus_ids = ScopusProfile.objects.filter(id_owner=staff)  # Fetch ScopusIDs associated with the staff member
        
        headers = {
            'Accept': 'application/json',
            'X-ELS-APIKey': SCOPUS_API_KEY,
        }
        
        payload = {
            'query': '',
            'view': 'complete',
            'suppressNavLinks': True,
            'field': 'link ref=scopus,prism:url,dc:title,prism:aggregationType,subtypeDescription,citedby-count,prism:publicationName,prism:isbn,prism:issn,prism:volume,prism:issueIdentifier,prism:pageRange,prism:coverDisplayDate,prism:doi,author'
        }
        
        # Build the query for Scopus API
        query_parts = []

        # Iterate through each scopus_id and construct the query part
        for scopus_id in scopus_ids:
            query_parts.append(f"au-id({scopus_id.scopus_author_id})")

        # Join all query parts with ' AND ' to form the complete query
        payload['query'] = ' OR '.join(query_parts)
        r = requests.get('https://api.elsevier.com/content/search/scopus', headers=headers, params=payload)
        json_response = r.json()
        
        # if json_response['error'] need to check if error, send proper response to frontend.
        
        return Response(json_response)

@method_decorator(cache_page(60*15), name='dispatch')
class GetScopusPublicationByScopusID(APIView):
    def get(self, request):
        scopus_id = self.request.query_params.get('scopus_id')  # Fetch 'staff_id' from query parameters
        
        headers = {
            'Accept': 'application/json',
            'X-ELS-APIKey': SCOPUS_API_KEY,
        }
        
        uri = f"https://api.elsevier.com/content/abstract/scopus_id/{scopus_id}"
        
        r = requests.get(uri, headers=headers)
        json_response = r.json()
        
        return Response(json_response)

@method_decorator(cache_page(60*60), name='dispatch')
class GetScopusYearlyPublicationCount(APIView):            
    def get(self, request):
        currYear = date.today().year
        filter_by = self.request.query_params.get('filter_by')
        filter_value = self.request.query_params.get('value')
        staffs = []
        scopus_profiles = []
        scopus_ids_query = ''
        if filter_value:
            if filter_by == "staff_id":
                staffs = Staff.objects.filter(staff_id=filter_value)
            if filter_by == "dept":
                staffs = Staff.objects.filter(department=filter_value)
            if filter_by == "school":
                staffs = Staff.objects.filter(school=filter_value)
            if not staffs:
                return Response({'error': f"Returned empty set from filter {filter_by}: {filter_value}"}, status=200)
            for staff in staffs:
                scopus_profiles = np.append(scopus_profiles, ScopusProfile.objects.filter(id_owner=staff)) 
            formatted_ids = [f"au-id({x.scopus_author_id})" for x in scopus_profiles]
            
            scopus_ids_query = " OR ".join(formatted_ids)
        
        headers = {
            'Accept': 'application/json',
            'X-ELS-APIKey': SCOPUS_API_KEY,
        }
        
        result = []
        
        for i in range(8):
            if filter_value:
                payload = {
                    'query': f"({scopus_ids_query}) AND PUBYEAR = {currYear - i}",
                    'view': 'complete',
                    'suppressNavLinks': True,
                    'count': '1',
                    'field': 'eid,dc:title'
                }
            else: 
                payload = {
                    'query': f"PUBYEAR = {currYear - i} AND af-id(60107208)",
                    'view': 'complete',
                    'suppressNavLinks': True,
                    'count': '1',
                    'field': 'eid,dc:title'
                }
            r = requests.get('https://api.elsevier.com/content/search/scopus', headers=headers, params=payload)
            yearly_publication = r.json()['search-results']['opensearch:totalResults']
            result.append({
                "year": f"{currYear - i}",
                "count": yearly_publication
            })
        return Response(result)