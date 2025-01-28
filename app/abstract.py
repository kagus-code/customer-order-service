from django.db import models


class TimeStampedModel(models.Model):
    """
    This is an abstract base class that allows us to put common fields created_at and updated_at that can be used in a number of models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        We put abstract=True in the Meta class so that the model will not be used to create any database table.
        Instead, when it is used as a base class for other models, its fields will be added to those of the child class.
        """

        abstract = True
