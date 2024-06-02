"""
Signals for updating counts in Company and Department models when changes occur in related models.

This module includes signals that listen to save and delete events on Department and Employee models.
It updates the counts of departments and employees in the Company model accordingly.

Author: Abdelmasry
"""

######################################################################
########################## I M P O R T S #############################
######################################################################
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Company, Department, Employee

######################################################################


######################################################################
########################## S I G N A L S #############################
######################################################################
@receiver(post_save, sender=Department)
def update_department_count(sender, instance, created, **kwargs):
    """
    Update the department count and total number of employees in the Company when a Department is created or updated.

    Args:
        sender (type): The model class.
        instance (Department): The actual instance being saved.
        created (bool): A boolean; True if a new record was created.
        **kwargs: Additional keyword arguments.
    """
    company = instance.company
    if created:
        company.no_of_deps += 1
        company.no_of_employees += instance.no_of_employees
    else:
        company.no_of_deps = Department.objects.filter(company=company).count()
    company.save()


@receiver(post_delete, sender=Department)
def decrease_department_count(sender, instance, **kwargs):
    """
    Update the department count and total number of employees in the Company when a Department is deleted.

    Args:
        sender (type): The model class.
        instance (Department): The actual instance being deleted.
        **kwargs: Additional keyword arguments.
    """
    company = instance.company
    company.no_of_deps -= 1
    company.no_of_employees -= instance.no_of_employees
    company.save()


@receiver(pre_save, sender=Employee)
def handle_employee_pre_save(sender, instance, **kwargs):
    """
    Handle changes to the Employee's company or department before saving.
    Updates the number of employees in the old and new company and department if changed.

    Args:
        sender (type): The model class.
        instance (Employee): The actual instance being saved.
        **kwargs: Additional keyword arguments.
    """
    if instance.pk:
        previous = Employee.objects.get(pk=instance.pk)
        if previous.company != instance.company:
            previous.company.no_of_employees -= 1
            instance.company.no_of_employees += 1
            previous.company.save()
            instance.company.save()
        if previous.department != instance.department:
            previous.department.no_of_employees -= 1
            instance.department.no_of_employees += 1
            previous.department.save()
            instance.department.save()


@receiver(post_save, sender=Employee)
def update_employee_counts(sender, instance, created, **kwargs):
    """
    Update the employee count in the Department and Company when an Employee is created or updated.

    Args:
        sender (type): The model class.
        instance (Employee): The actual instance being saved.
        created (bool): A boolean; True if a new record was created.
        **kwargs: Additional keyword arguments.
    """
    company = instance.company
    department = instance.department
    if created:
        department.no_of_employees += 1
        company.no_of_employees += 1
    else:
        department.no_of_employees = Employee.objects.filter(
            department=department
        ).count()
        company.no_of_employees = Employee.objects.filter(company=company).count()
    department.save()
    company.save()


@receiver(post_delete, sender=Employee)
def decrease_employee_counts(sender, instance, **kwargs):
    """
    Update the employee count in the Department and Company when an Employee is deleted.

    Args:
        sender (type): The model class.
        instance (Employee): The actual instance being deleted.
        **kwargs: Additional keyword arguments.
    """
    department = instance.department
    company = instance.company
    department.no_of_employees -= 1
    company.no_of_employees -= 1
    department.save()
    company.save()


######################################################################
