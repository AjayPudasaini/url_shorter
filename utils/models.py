from django.db import models

class DateTimeAbstract(models.Model):
    """
    Abstract base model class to track creation and last update timestamps.

    Attributes:
        created_at (DateTimeField): The datetime when the instance was created.
        updated_at (DateTimeField): The datetime when the instance was last updated.

    Meta:
        abstract (bool): Indicates that this model is abstract and not to be used to create database tables directly.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True