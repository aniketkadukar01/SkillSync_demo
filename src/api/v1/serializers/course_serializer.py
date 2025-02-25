from rest_framework import serializers
from course.models import (
    CourseCategory,
    Course,
    Assignee,
    Module,
)

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['category_name']


class CourseSerializer(serializers.ModelSerializer):
    
    def to_representation(self, instance):
        """
        This method is taken the current course instance and convert into custom representation.
        """
        data = super().to_representation(instance)
        if data['category']:
            data['category'] = str(instance.category.category_name)
        if data['status']:
            data['status'] = str(instance.status.choice_name)
        return data
    
    class Meta:
        model = Course
        fields = ['course_title', 'is_mandatory', 'category', 'no_of_assignee', 'course_duration', 'status',]
        extra_fields = {
            'no_of_assignee': {'read_only': True},
            'course_duration': {'read_only': True},
        }


class AssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignee
        fields = []


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['course', 'module_name', 'module_number']
        extra_kwargs = {
            'course': {'write_only': True},
        }
