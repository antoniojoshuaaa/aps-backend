from django.urls import path
from .views import StaffList, GetStaffById


urlpatterns = [
    path('', StaffList.as_view(), name="staff-list-view"),
    path('profile/<str:staff_id>/', GetStaffById.as_view(), name="staff-by-id"),
]
