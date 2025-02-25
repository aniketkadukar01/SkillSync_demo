from rest_framework import serializers
from course.models import (
    CourseCategory,
    Course,
    Assignee,
    Module,
    Lesson,
    Question,
    QuestionOptions,
    Answer,
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
        fields = ['course', 'user', 'type', 'designation', 'department', 'grade']


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


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'answer', 'is_correct']
