"""
Views for managing Company, Department, and Employee models using Django REST Framework APIViews.

This module defines APIViews for Company, Department, and Employee models, providing
list, retrieve, create, update, and delete functionality.

Author: Abdelmasry
"""

######################################################################
########################## I M P O R T S #############################
######################################################################
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser, IsManagerUser, IsEmployeeUser
from .models import Company, Department, Employee, UserAccounts
from .serializers import (
    CompanySerializer,
    DepartmentSerializer,
    EmployeeSerializer,
    UserAccountsSerializer,
)

######################################################################


######################################################################
############################ V I E W S ###############################
######################################################################


class UserAccountsView(APIView):
    """
    A view for creating, retrieving, updating, and deleting UserAccounts instances.

    Only accessible by superusers.
    """

    serializer_class = UserAccountsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, id=None):
        """
        Retrieve a single UserAccounts instance or a list of all UserAccounts instances.

        Args:
            request (Request): The HTTP request.
            id (int, optional): The primary key of the UserAccounts instance to retrieve. Defaults to None.

        Returns:
            Response: HTTP response containing UserAccounts data.
        """
        if id:
            user = get_object_or_404(UserAccounts, pk=id)
            serializer = UserAccountsSerializer(user)
            return Response(serializer.data)
        else:
            queryset = UserAccounts.objects.all()
            serializers = UserAccountsSerializer(queryset, many=True)
            return Response(
                {"status": "success", "Users": serializers.data}, status=200
            )

    def post(self, request):
        """
        Create a new UserAccounts instance.

        Args:
            request (Request): The HTTP request.

        Returns:
            Response: HTTP response containing created UserAccounts data or errors.
        """
        serializer = UserAccountsSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        Delete a UserAccounts instance.

        Args:
            request (Request): The HTTP request.
            id (int): The primary key of the UserAccounts instance to delete.

        Returns:
            Response: HTTP 204 No Content status code on successful deletion.
        """
        user = get_object_or_404(UserAccounts, pk=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        """
        Create a new user account with the provided data.

        Args:
            serializer (UserAccountsSerializer): The serializer with validated data.
        """
        serializer.save()


class CompanyAPIView(APIView):
    """
    A view for viewing and editing Company instances.

    Provides list, retrieve, create, update, and delete actions for Company model.

    URL endpoints:
    - List all companies: /company/
    - Retrieve a single company: /company/{id}/
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]  # Only admin users can access this view

    def get(self, request, pk=None):
        """
        Retrieve a single Company instance or a list of all Company instances.

        Args:
            request (Request): The HTTP request.
            pk (int, optional): The primary key of the Company instance to retrieve. Defaults to None.

        Returns:
            Response: HTTP response containing Company data.
        """
        if pk:
            company = get_object_or_404(Company, pk=pk)
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        else:
            queryset = Company.objects.all()
            serializers = CompanySerializer(queryset, many=True)
            return Response(
                {"status": "success", "Companies": serializers.data}, status=200
            )

    def post(self, request):
        """
        Create a new Company instance.

        Args:
            request (Request): The HTTP request.

        Returns:
            Response: HTTP response containing created Company data or errors.
        """
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            company = serializer.save()
            return Response(
                {"company": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update a Company instance.

        Args:
            request (Request): The HTTP request.
            pk (int): The primary key of the Company instance to update.

        Returns:
            Response: HTTP response containing updated Company data or errors.
        """
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            company = serializer.save()
            return Response(
                {"company": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a Company instance.

        Args:
            request (Request): The HTTP request.
            pk (int): The primary key of the Company instance to delete.

        Returns:
            Response: HTTP 204 No Content status code on successful deletion.
        """
        company = get_object_or_404(Company, pk=pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DepartmentAPIView(APIView):
    """
    A view for viewing and editing Department instances.

    Provides list, retrieve, create, update, and delete actions for Department model.

    URL endpoints:
    - List all departments: /department/
    - Retrieve a single department: /department/{id}/
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    permission_classes = [
        IsManagerUser | IsAdminUser
    ]  # Admin and Manager users can access this view

    def get(self, request, pk=None):
        """
        Retrieve a single Department instance or a list of all Department instances.

        Args:
            request (Request): The HTTP request.
            pk (int, optional): The primary key of the Department instance to retrieve. Defaults to None.

        Returns:
            Response: HTTP response containing Department data.
        """
        if pk:
            department = get_object_or_404(Department, pk=pk)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data)
        else:
            queryset = Department.objects.all()
            serializers = DepartmentSerializer(queryset, many=True)
            return Response(
                {"status": "success", "Departments": serializers.data}, status=200
            )

    def post(self, request):
        """
        Create a new Department instance.

        Args:
            request (Request): The HTTP request.

        Returns:
            Response: HTTP response containing created Department data or errors.
        """

        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            department = serializer.save()
            return Response(
                {"department": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update a Department instance.

        Args:
            request (Request): The HTTP request.
            pk (int): The primary key of the Department instance to update.

        Returns:
            Response: HTTP response containing updated Department data or errors.
        """
        department = get_object_or_404(Department, pk=pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            department = serializer.save()
            return Response(
                {"department": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a Department instance.

        Args:
            request (Request): The HTTP request.
            pk (int): The primary key of the Department instance to delete.

        Returns:
            Response: HTTP 204 No Content status code on successful deletion.
        """
        department = get_object_or_404(Department, pk=pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeAPIView(APIView):
    """
    A view for viewing and editing Employee instances.

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
    permission_classes = [
        IsAuthenticated,
        IsAdminUser | IsManagerUser | IsEmployeeUser,
    ]  # All roles can access this view

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), IsEmployeeUser()]
        return [
            IsAuthenticated(),
            IsAdminUser | IsManagerUser,
        ]  # Allow only Admin or Manager for other methods

    def get(self, request, pk=None):
        """
        Retrieve a single Employee instance or a list of all Employee instances.

        Args:
            request (Request): The HTTP request.
            pk (int, optional): The primary key of the Employee instance to retrieve. Defaults to None.

        Returns:
            Response: HTTP response containing Employee data.
        """
        if pk:
            employee = get_object_or_404(Employee, pk=pk)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        else:
            queryset = Employee.objects.all()
            serializers = EmployeeSerializer(queryset, many=True)
            return Response(
                {"status": "success", "Employees": serializers.data}, status=200
            )

    def post(self, request):
        """
        Create a new Employee instance.

        Args:
            request (Request): The HTTP request.

        Returns:
            Response: HTTP response containing created Employee data or errors.
        """
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            return Response(
                {"employee": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update an Employee instance.

        Args:
            request (Request): The HTTP request.
            pk (int): The primary key of the Employee instance to update.

        Returns:
            Response: HTTP response containing updated Employee data or errors.
        """
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            return Response(
                {"employee": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete an Employee instance.

        Args:
            request (Request): The HTTP request.
            pk (int): The primary key of the Employee instance to delete.

        Returns:
            Response: HTTP 204 No Content status code on successful deletion.
        """
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
