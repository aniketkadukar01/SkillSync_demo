from rest_framework import serializers
from course.models import (
    CourseCategory,
    Course,
    Assignee,
    Module,
    Lesson,
    Question,
    QuestionOptions,
)
from user.models import User
from django.db.models import Sum

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['category_name']


class CourseSerializer(serializers.ModelSerializer):
    no_of_assignee = serializers.SerializerMethodField()
    course_duration = serializers.SerializerMethodField()

    def get_no_of_assignee(self, obj):
        return Assignee.objects.filter(course=obj).count()

    def get_course_duration(self, obj):
         return Lesson.objects.filter(module__course=obj).aggregate(total_duration=Sum('lesson_duration'))['total_duration']

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
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['course'] = str(instance.course.course_title) if data['course'] else data['course']
        data['user'] = f"{instance.user.first_name} {instance.user.last_name}" if data['user'] else data['user']
        data['type'] = str(instance.type.choice_name) if data['type'] else data['type']
        return data

    class Meta:
        model = Assignee
        fields = ['course', 'user', 'type', 'department', 'grade']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['course', 'module_name', 'module_number']
        extra_kwargs = {
            'course': {'write_only': True},
        }


class CourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['module', 'lesson_name', 'lesson_number', 'lesson_duration', 'lesson_description', 'media']


class CourseQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['module', 'answer_type', 'question']


class QuestionOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOptions
        fields = ['question', 'options']
