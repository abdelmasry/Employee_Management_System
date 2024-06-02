from django.urls import path
from .views import (
    CompanyAPIView,
    DepartmentAPIView,
    EmployeeAPIView,
    UserAccountsView,
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = "main"

urlpatterns = [
    path("company/", CompanyAPIView.as_view(), name="company-list"),
    path("company/<int:pk>/", CompanyAPIView.as_view(), name="company-detail"),
    path("department/", DepartmentAPIView.as_view(), name="department-list"),
    path("department/<int:pk>/", DepartmentAPIView.as_view(), name="department-detail"),
    path("employee/", EmployeeAPIView.as_view(), name="employee-list"),
    path("employee/<int:pk>/", EmployeeAPIView.as_view(), name="employee-detail"),
    path("user/", UserAccountsView.as_view(), name="user-list"),
    path("user/<int:id>/", UserAccountsView.as_view(), name="user-detail"),
    path("token/", obtain_auth_token, name="api_token_auth"),
]
