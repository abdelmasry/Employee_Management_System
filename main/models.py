"""
Module for defining the models for the application.

This module includes definitions for the UserAccounts, Company, Department,
and Employee models. Each model is documented with its fields and any custom
validation or save logic.

Author: Abdelmasry
"""

######################################################################
########################## I M P O R T S #############################
######################################################################
from django.db import models
from django.core.validators import MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

######################################################################


######################################################################
########################### M O D E L S ##############################
######################################################################


class UserAccountsManager(BaseUserManager):
    def create_user(self, username, email, role, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, role, password=None):
        user = self.create_user(username, email, role, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccounts(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with AbstractBaseUser and PermissionsMixin.
    """

    username = models.CharField(max_length=64, unique=True, null=False)
    email = models.EmailField(max_length=64, unique=True, null=False)
    roles = [
        ("ADMIN", "Admin"),
        ("MANAGER", "Manager"),
        ("EMPLOYEE", "Employee"),
    ]
    role = models.CharField(max_length=10, choices=roles)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountsManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "role"]

    def __str__(self):
        return self.username


class Company(models.Model):
    """
    Model representing a company.
    """

    company_name = models.CharField(max_length=64, unique=True, null=False)
    no_of_deps = models.IntegerField(default=0)
    no_of_employees = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(9999)]
    )

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.company_name


class Department(models.Model):
    """
    Model representing a department within a company.
    """

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=64, unique=True, null=False)
    no_of_employees = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(9999)]
    )

    class Meta:
        ordering = ["company"]
        unique_together = ("company", "department_name")

    def clean(self):
        """
        Custom validation to ensure that the combination of company and department_name is unique.
        """
        if self.__class__.objects.filter(
            company=self.company, department_name=self.department_name
        ).exists():
            raise ValidationError(
                "A department with the same name already exists for this company."
            )

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure the department name includes the company name.
        """
        if not self.department_name.__contains__(self.company.company_name):
            self.department_name = f"{self.company.company_name}_{self.department_name}"

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.department_name


class Employee(models.Model):
    """
    Model representing an employee.
    """

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    stages = [
        ("APPLICATION_RECEIVED", "Application Received"),
        ("INTERVIEW_SCHEDULED", "Interview Scheduled"),
        ("HIRED", "Hired"),
        ("NOT_ACCEPTED", "Not Accepted"),
    ]
    status = models.CharField(max_length=20, choices=stages)
    name = models.CharField(max_length=64, null=False)
    email = models.CharField(max_length=64, unique=True, null=False)
    mobile_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
        null=False,
        blank=False,
    )
    address = models.CharField(max_length=255, null=False)
    designation = models.CharField(max_length=64, null=False)  # Position/Title
    hired_on = models.DateField(null=True, blank=True)  # Only if hired
    days_employed = models.PositiveIntegerField(
        null=True, blank=True
    )  # Field to store calculated value

    class Meta:
        ordering = ["id"]

    def clean(self):
        """
        Custom validation to ensure hired_on is provided if status is "HIRED".
        """
        if self.status == "HIRED" and not self.hired_on:
            raise ValidationError(
                "A hire date must be provided if the status is 'Hired'."
            )

    def save(self, *args, **kwargs):
        """
        Override the save method to calculate days employed if status is "HIRED".
        """
        if self.status == "HIRED" and self.hired_on:
            self.days_employed = (timezone.now().date() - self.hired_on).days
        else:
            self.days_employed = None
        super().save(*args, **kwargs)


######################################################################
