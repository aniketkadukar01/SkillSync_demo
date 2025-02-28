from rest_framework import serializers
from course.models import (
    CourseCategory,
    Course,
    Assignee,
    Module,
    Lesson,
    Question,
    QuestionOptions,
    UserScore,
    UserAnswer,
)
from user.models import User
from django.db.models import Sum


class CourseCategorySerializer(serializers.ModelSerializer):
    """This Serializer is used for Course-Category operation"""

    class Meta:
        model = CourseCategory
        fields = ['category_name']


class CourseSerializer(serializers.ModelSerializer):
    """This Serializer is used for Course operation"""

    """SerializerMethodField method indicates that value of these field will be determined,
        by a method within the serializer."""
    no_of_assignee = serializers.SerializerMethodField()
    course_duration = serializers.SerializerMethodField()

    def get_no_of_assignee(self, obj):
        """
        This is the method that provides the value for the no_of_assignee field.
        :param obj: current instance which passed to become serialized.
        :return: calculated value.
        """
        return Assignee.objects.filter(course=obj).count()

    def get_course_duration(self, obj):
        """
        This is the method that provides the value for the course_duration field.
        :param obj: current instance which passed to become serialized.
        :return: calculated value.
        """
        total_duration = Lesson.objects.filter(module__course=obj).aggregate(total_duration=Sum('lesson_duration'))['total_duration']
        if total_duration:
            total_seconds = total_duration.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            return f'{hours}hr {minutes}min {seconds}sec'
        else:
            return "0hr 0min 0sec"

    def to_representation(self, instance):
        """
        This method executes during the serialization process of data.
        If we want to change the data of instance or want to make any changes before the response sent.
        :param instance: current instance which passed to become serialized.
        :return: serialized data.
        """
        data = super().to_representation(instance)
        data['category'] = str(instance.category.category_name) if data['category'] else data['category']
        data['status'] = str(instance.status.choice_name) if data['status'] else data['status']
        return data
    
    class Meta:
        model = Course
        fields = ['course_title', 'is_mandatory', 'category', 'no_of_assignee', 'course_duration', 'status',]
        extra_kwargs = {
            'no_of_assignee': {'read_only': True},
            'course_duration': {'read_only': True},
        }


class AssigneeSerializer(serializers.ModelSerializer):
    """This Serializer is used for Assignee operation"""

    def to_representation(self, instance):
        """
        This method executes during the serialization process of data.
        If we want to change the data of instance or want to make any changes before the response sent.
        :param instance: current instance which passed to become serialized.
        :return: serialized data.
        """
        data = super().to_representation(instance)
        data['course'] = str(instance.course.course_title) if data['course'] else data['course']
        data['user'] = f"{instance.user.first_name} {instance.user.last_name}" if data['user'] else data['user']
        return data

    class Meta:
        model = Assignee
        fields = ['course', 'user',]


class ModuleSerializer(serializers.ModelSerializer):
    """This Serializer is used for Module operation"""

    class Meta:
        model = Module
        fields = ['course', 'module_name', 'module_number']
        extra_kwargs = {
            'course': {'write_only': True},
        }


class CourseLessonSerializer(serializers.ModelSerializer):
    """This Serializer is used for Course Lesson operation"""

    class Meta:
        model = Lesson
        fields = ['module', 'lesson_name', 'lesson_number', 'lesson_duration', 'lesson_description', 'media']


class CourseQuestionSerializer(serializers.ModelSerializer):
    """This Serializer is used for Course Question operation"""

    class Meta:
        model = Question
        fields = ['module', 'answer_type', 'question']


class QuestionOptionsSerializer(serializers.ModelSerializer):
    """This Serializer is used for Question Options operation"""

    class Meta:
        model = QuestionOptions
        fields = ['question', 'options']


class UserScoreSerializer(serializers.ModelSerializer):
    """This Serializer is used for User Score operation"""

    class Meta:
        model = UserScore
        fields = ['user', 'lesson', 'attempts', 'score_achieved', 'test_result']


class UserAnswerSerializer(serializers.ModelSerializer):
    """This Serializer is used for User Answer operation"""

    class Meta:
        model = UserAnswer
        fields = ['user', 'answer', 'user_answer']
