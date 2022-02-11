
from django.db import models


class Person(models.Model):
    """Model for testing purposes."""

    name = models.CharField(max_length=30, verbose_name="Person's name")

    class Meta:
        verbose_name = 'person'
        verbose_name_plural = 'persons'

    def __str__(self):
        return self.name
