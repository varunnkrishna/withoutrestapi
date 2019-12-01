from django.urls import path, re_path
from empdata import views

urlpatterns = [
    # path( 'api/<int:id>/', views.EmployeeDetailCBV.as_view()),
    path( 'api/', views.EmployeeCRUDCBV.as_view()),
]
