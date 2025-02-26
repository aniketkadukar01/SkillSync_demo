from course.models import (
    CourseCategory,
    Course,
    Module,
    Lesson,
    Question,
    QuestionOptions,
    Assignee,
)
from rest_framework import viewsets
from ..serializers.course_serializer import (
    CourseCategorySerializer,
    CourseSerializer,
    ModuleSerializer,
    CourseLessonSerializer,
    CourseQuestionSerializer,
    QuestionOptionsSerializer,
    AssigneeSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from user.models import User
from ..decorators.course_decorators import resolve_assignee_name


class CourseCategoryView(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'Category created successfully.'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response({'error': f'Category cannot update.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'Category deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'Course created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'Course deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class ModuleView(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'Module created successfully.'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            if 'module_number' in serializer.validated_data:
                Module.objects.filter(course=instance.course,
                                      module_number__gte=serializer.validated_data['module_number']).update(
                    module_number=F('module_number') + 1)
            serializer.save()
            return Response({'success': 'Module update successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': 'Module Deleted Successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CourseLessonView(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = CourseLessonSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'Lesson created successfully.'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            if 'lesson_number' in serializer.validated_data:
                Lesson.objects.filter(module=instance.module,
                                      lesson_number__gte=serializer.validated_data['lesson_number']).update(
                    lesson_number=F('lesson_number') + 1)
            serializer.save()
            return Response({'success': 'Lesson update successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': 'Lesson Deleted Successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CourseQuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = CourseQuestionSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'Question created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'Question deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class QuestionOptionsView(viewsets.ModelViewSet):
    queryset = QuestionOptions.objects.all()
    serializer_class = QuestionOptionsSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'Question option created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'Question option deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class AssigneeView(viewsets.ModelViewSet):
    queryset = Assignee.objects.all()
    serializer_class = AssigneeSerializer

    @resolve_assignee_name
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'Assignee created successfully.'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response({'error': f'Assignee cannot update.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'Assignee deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
