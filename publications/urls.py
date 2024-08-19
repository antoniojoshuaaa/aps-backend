from django.urls import path
from .views import GetScopusPublicationByAffiliation, GetScopusPublicationByScopusID, GetScopusYearlyPublicationCount
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('', GetScopusPublicationByAffiliation.as_view(), name="get-scopus-publication-by-affiliation"),
    path('scopus_id/', GetScopusPublicationByScopusID.as_view(), name="get-scopus-publication-by-scopus-id"),
    path('count/yearly/', GetScopusYearlyPublicationCount.as_view(), name="get-scopus-yearly-publication-count")
]
