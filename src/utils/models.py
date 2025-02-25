from django.db import models
from .choices import CHOICE_TYPES

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"created_at: {self.created_at} and last_update: {self.updated_at}"

    class Meta:
        abstract = True


class Choice(BaseModel):
    choice_name = models.CharField(max_length=150,)
    choice_type = models.CharField(max_length=255, choices=CHOICE_TYPES,)

    def __str__(self):
        return f"{self.choice_name}"

    class Meta:
        db_table = 'choices'
        unique_together = ('choice_name', 'choice_type',)
