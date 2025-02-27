from django.urls import path, include
from rest_framework import routers
from .views import (
    user_view,
    course_view,
)


router = routers.DefaultRouter()
router.register(r'login', user_view.LoginView, basename='login')
router.register(r'Create-refresh-token', user_view.CreateRefreshTokenView, basename='Create new refresh token')
router.register(r'logout', user_view.LogoutView, basename='logout')
router.register(r"logout-all", user_view.LogoutAllView, basename='logout from all devices')
router.register(r'users', user_view.UserView, basename='users')
router.register(r'course-categories', course_view.CourseCategoryView, basename='course_categories')
router.register(r'courses', course_view.CourseView, basename='courses')
router.register(r'modules', course_view.ModuleView, basename='modules')
router.register(r'lessons', course_view.CourseLessonView, basename='lessons')
router.register(r'questions', course_view.CourseQuestionView, basename='questions')
router.register(r'questions-options', course_view.QuestionOptionsView, basename='questions_options')
router.register(r'assignees', course_view.AssigneeView, basename='assignees')


urlpatterns = [
    path('', include(router.urls)),
    path('forget-password/', user_view.ForgetPasswordView.as_view(), name='forget_password'),
    path('reset-password/<str:encode_user_id>/<str:encode_user_token>/', user_view.ResetPasswordView.as_view(), name='reset_password')
]
