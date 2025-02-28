from django.contrib import admin
from .models import (
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
from django.utils.translation import gettext_lazy as _

# Register your models here.

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    fieldsets = ((_("Course Category info"), {"fields": ("category_name",)}),)
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("category_name",),},),)
    list_display = ("category_name",)
    ordering = ("category_name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fieldsets = ((_("Course info"), {"fields": ("course_title", "is_mandatory", "category", "status",)}),)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "course_title",
                    "is_mandatory",
                    "category",
                    "status",
                ),
            },
        ),
    )
    list_display = ("course_title", "is_mandatory", "category",)
    list_filter = ("category", 'status',)


@admin.register(Assignee)
class AssigneeAdmin(admin.ModelAdmin):
    fieldsets = ((_("Assignee info"), {"fields": ("course", "user",)}),)
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("course", "user",),},),)
    list_display = ("course", "user",)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    fieldsets = ((_("Module info"), {"fields": ("course", "module_name", "module_number",)}),)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "course",
                    "module_name",
                    "module_number",
                ),
            },
        ),
    )
    list_display = ("course", "module_name", "module_number",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("Personal info"),
            {
                "fields": (
                    "module",
                    "lesson_name",
                    "lesson_number",
                    "lesson_duration",
                    "lesson_description",
                    "media",
                )
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "module",
                    "lesson_name",
                    "lesson_number",
                    "lesson_duration",
                ),
            },
        ),
    )
    list_display = ("module", "lesson_name", "lesson_number",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = ((_("Question info"), {"fields": ("module", "answer_type", "question",)}),)
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("module", "answer_type", "question",),},),)
    list_display = ("module", "answer_type", "question",)
    list_filter = ("answer_type",)


@admin.register(QuestionOptions)
class QuestionOptions(admin.ModelAdmin):
    fieldsets = ((_("Question options info"), {"fields": ("question", "options", "is_correct",)}),)
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("question", "options", "is_correct",),},),)
    list_display = ("question", "options", "is_correct",)
    list_filter = ("is_correct",)


@admin.register(UserScore)
class UserScoreAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("User Score info"),
            {
                "fields": (
                    "user",
                    "lesson",
                    "attempts",
                    "score_achieved",
                    "test_result",
                )
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "user",
                    "lesson",
                    "attempts",
                    "score_achieved",
                    "test_result",
                ),
            },
        ),
    )
    list_display = ("user", "attempts", "score_achieved",)
    list_filter = ("test_result",)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    fieldsets = ((_("User answer info"), {"fields": ("user", "answer", "user_answer",)}),)
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("user", "answer", "user_answer",), },),)
    list_display = ("user", "answer", "user_answer",)
