from django.db import models
from utils.models import BaseModel, Choice
from .choices import COURSE_CATEGORY_CHOICES
from user.models import User

# Create your models here.

class CourseCategory(BaseModel):
    category_name = models.CharField(max_length=150, unique=True, choices=COURSE_CATEGORY_CHOICES)

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        db_table = 'course_categories'


class Course(BaseModel):
    course_title = models.CharField(max_length=255,)
    is_mandatory = models.BooleanField(blank=True, null=True, default=False,)
    category = models.ForeignKey(
        CourseCategory,
        on_delete=models.SET_NULL,
        related_name='course_category',
        blank=True,
        null=True,
    )
    no_of_assignee = models.PositiveIntegerField(blank=True, null=True,)
    course_duration = models.DurationField(blank=True, null=True,)
    status = models.ForeignKey(
        Choice,
        on_delete=models.SET_NULL,
        related_name='course_status',
        limit_choices_to={'choice_type': 'status'},
        null=True,
    )

    def __str__(self):
        return f'Course is {self.course_title} and duration {self.course_duration}'

    class Meta:
        db_table = 'courses'


class Assignee(BaseModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        related_name='assignee_course',
        blank=True,
        null=True,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='assignee_user',
    )
    type = models.ForeignKey(
        Choice,
        on_delete=models.SET_NULL,
        related_name='assignee_type',
        limit_choices_to={'choice_type': 'assignee'},
        null=True,
    )
    designation = models.CharField(max_length=255, blank=True, null=True,)
    department = models.CharField(max_length=200, blank=True, null=True,)
    grade = models.CharField(max_length=2,)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} and designation is {self.designation}'

    class Meta:
        db_table = 'assignees'


class Module(BaseModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='module_course',
    )
    module_name = models.CharField(max_length=255,)
    module_number = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.module_name} {self.module_number}'

    class Meta:
        db_table = 'modules'


class Lesson(BaseModel):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lesson_module',
    )
    lesson_name = models.CharField(max_length=255,)
    lesson_number = models.PositiveIntegerField(unique=True,)
    lesson_duration = models.DurationField()
    description = models.TextField(max_length=500, blank=True, null=True,)
    media = models.FileField(blank=True, null=True, upload_to='media/lessons_media',)

    def __str__(self):
        return f'{self.lesson_name} {self.lesson_number}'

    class Meta:
        db_table = ' lessons'


class Question(BaseModel):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='question_module',
    )
    answer_type = models.ForeignKey(
        Choice,
        on_delete=models.SET_NULL,
        related_name='question_answer_type',
        limit_choices_to={'choice_type': 'answer'},
        null=True,
    )
    question = models.TextField(max_length=300,)

    def __str__(self):
        return f'{self.question}'

    class Meta:
        db_table = 'questions'


class QuestionOptions(BaseModel):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='question_options_question',
    )
    options = models.CharField(max_length=255,)

    def __str__(self):
        return f'{self.options}'

    class Meta:
        db_table = 'question_options'


class Answer(BaseModel):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answer_question',
    )
    answer = models.CharField(max_length=255, blank=True, null=True,)
    is_correct = models.BooleanField(blank=True, null=True,)

    def __str__(self):
        return f'{self.answer} {self.is_correct}'

    class Meta:
        db_table = 'answers'
