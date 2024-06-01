"""
Views for managing Company, Department, and Employee models using Django REST Framework viewsets.

This module defines viewsets for Company, Department, and Employee models, providing
list, retrieve, create, update, and delete functionality.

Author: Abdelmasry
"""

######################################################################
########################## I M P O R T S #############################
######################################################################
from django.http import Http404
from rest_framework.response import Response
from rest_framework import viewsets, status, exceptions
from .models import Company, Department, Employee
from .serializers import CompanySerializer, DepartmentSerializer, EmployeeSerializer
######################################################################

######################################################################
############################ V I E W S ###############################
######################################################################
class CompanyViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Company instances.

    Provides list, retrieve, create, update, and delete actions for Company model.

    URL endpoints:
    - List all companies: /company/
    - Retrieve a single company: /company/{id}/
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def destroy(self, request, *args, **kwargs):
        """
        Handle the DELETE request for a Company instance.

        Args:
            request (Request): The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Raises:
            MethodNotAllowed: Always raises this exception as DELETE is not allowed for Company instances.
        """
        raise exceptions.MethodNotAllowed("DELETE")


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Department instances.

    Provides list, retrieve, create, update, and delete actions for Department model.

    URL endpoints:
    - List all departments: /department/
    - Retrieve a single department: /department/{id}/
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Employee instances.

    Provides list, retrieve, create, update, and delete actions for Employee model.

    URL endpoints:
    - List all employees: /employee/
    - Retrieve a single employee: /employee/{id}/
    - Create a new employee: /employee/
    - Update an existing employee: /employee/{id}/
    - Delete an employee: /employee/{id}/
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def delete(self, request, pk, format=None):
        """
        Delete an Employee instance.

        Args:
            request (Request): The HTTP request.
            pk (int): The primary key of the Employee instance to delete.
            format (str): The format suffix, if any.

        Returns:
            Response: HTTP 204 No Content status code on successful deletion.
        """
        try:
            employee = self.get_object(pk)
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            raise Http404("Employee not found")
######################################################################