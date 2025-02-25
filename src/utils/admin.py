from django.contrib import admin
from .models import Choice

# Register your models here.

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("choice_name", "choice_type")}),)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("choice_name", "choice_type",),
            },
        ),
    )
    list_display = ['choice_name', 'choice_type',]
    list_filter = ("choice_type",)
    search_fields = ("choice_type",)
