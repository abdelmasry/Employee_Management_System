from django.urls import path
from . import serializers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, DepartmentViewSet, EmployeeViewSet

app_name = "main"

router = DefaultRouter()
router.register(r"company", CompanyViewSet)
router.register(r"department", DepartmentViewSet)
router.register(r"employee", EmployeeViewSet)

app_name = "main"

urlpatterns = [
    path("", include(router.urls)),
]
