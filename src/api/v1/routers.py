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


urlpatterns = [
    path('', include(router.urls)),
]
