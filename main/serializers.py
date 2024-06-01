"""
Serializers for transforming model instances into JSON and validating incoming data.

This module includes serializers for the Company, Department, and Employee models.
Each serializer is documented with its fields and any custom validation or save logic.

Author: Abdelmasry
"""
######################################################################
########################## I M P O R T S #############################
######################################################################
from rest_framework import serializers
from .models import Company, Department, Employee
######################################################################

######################################################################
###################### S E R I A L I Z E R S #########################
######################################################################
class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for the Company model.
    Transforms Company instances into JSON and validates incoming data.
    """

    class Meta:
        model = Company
        fields = "__all__"

    def create(self, validated_data):
        """
        Create a new Company instance with custom validation.

        Args:
            validated_data (dict): Validated data for the new Company instance.

        Returns:
            Company: The created Company instance.

        Raises:
            serializers.ValidationError: If a company with the same name already exists.
        """
        company_name = validated_data.get("company_name")

        if Company.objects.filter(company_name=company_name).exists():
            raise serializers.ValidationError(
                "A company with this name already exists."
            )

        company = Company.objects.create(**validated_data)
        return company


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Department model.
    Transforms Department instances into JSON and validates incoming data.
    """

    company = serializers.SlugRelatedField(
        queryset=Company.objects.all(), slug_field="company_name"
    )

    class Meta:
        model = Department
        fields = "__all__"

    def create(self, validated_data):
        """
        Create a new Department instance.

        Args:
            validated_data (dict): Validated data for the new Department instance.

        Returns:
            Department: The created Department instance.
        """
        return Department.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing Department instance.

        Args:
            instance (Department): The Department instance to update.
            validated_data (dict): Validated data for updating the Department instance.

        Returns:
            Department: The updated Department instance.
        """
        instance.company = validated_data.get("company", instance.company)
        instance.department_name = validated_data.get(
            "department_name", instance.department_name
        )
        instance.company.no_of_employees += (
            validated_data.get("no_of_employees", instance.no_of_employees)
            - instance.no_of_employees
        )
        instance.no_of_employees = validated_data.get(
            "no_of_employees", instance.no_of_employees
        )
        instance.save()
        return instance


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Employee model.
    Transforms Employee instances into JSON and validates incoming data.
    """

    company = serializers.SlugRelatedField(
        queryset=Company.objects.all(), slug_field="company_name"
    )
    department = serializers.SlugRelatedField(
        queryset=Department.objects.all(), slug_field="department_name"
    )

    class Meta:
        model = Employee
        fields = "__all__"

    def validate(self, data):
        """
        Custom validation to ensure that the department belongs to the given company.

        Args:
            data (dict): The validated data.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the department does not belong to the given company.
        """
        company = data.get("company")
        department = data.get("department")
        if department.company != company:
            raise serializers.ValidationError(
                "The department does not belong to the given company."
            )
        return data

    def create(self, validated_data):
        """
        Create a new Employee instance.

        Args:
            validated_data (dict): Validated data for the new Employee instance.

        Returns:
            Employee: The created Employee instance.
        """
        return Employee.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing Employee instance.

        Args:
            instance (Employee): The Employee instance to update.
            validated_data (dict): Validated data for updating the Employee instance.

        Returns:
            Employee: The updated Employee instance.
        """
        instance.company = validated_data.get("company", instance.company)
        instance.department = validated_data.get("department", instance.department)
        instance.status = validated_data.get("status", instance.status)
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.mobile_number = validated_data.get(
            "mobile_number", instance.mobile_number
        )
        instance.address = validated_data.get("address", instance.address)
        instance.designation = validated_data.get("designation", instance.designation)
        instance.hired_on = validated_data.get("hired_on", instance.hired_on)
        instance.days_employed = validated_data.get(
            "days_employed", instance.days_employed
        )
        instance.save()
        return instance
######################################################################