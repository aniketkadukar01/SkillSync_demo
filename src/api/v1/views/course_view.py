from course.models import (
    CourseCategory,
    Course,
    Module,
    Lesson,
    Question,
    QuestionOptions,
    Assignee,
    UserScore,
    UserAnswer,
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
    UserScoreSerializer,
    UserAnswerSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from user.models import User
from ..decorators.course_decorators import resolve_assignee_name
from ..paginations.course_pagination import AssigneePagination


class CourseCategoryView(viewsets.ModelViewSet):
    """This View is used for Course-Category api."""

    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create and return success message.
        :param request: course-category data.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().create(request, *args, **kwargs)
        return Response({'success': f'Category created successfully.'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        This method is used to update and return success message.
        :param request: course-category data.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        return Response({'error': f'Category cannot update.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        This method is used to destroy and return success message.
        :param request: none.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'Category deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CourseView(viewsets.ModelViewSet):
    """This View is used for Course api."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create and return success message.
        :param request: course data.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().create(request, *args, **kwargs)
        return Response({'success': f'Course created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
        This method is used to destroy and return success message.
        :param request: none.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'Course deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class ModuleView(viewsets.ModelViewSet):
    """This View is used for Module api."""

    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create and return success message and adjust the module_number accordingly.
        :param request: Module data.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().create(request, *args, **kwargs)
        return Response({'success': f'Module created successfully.'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        This method is used to update and return success message and adjust the module_number accordingly.
        :param request: Module data.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
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
        """
        This method is used to destroy and return success message.
        :param request: none.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().destroy(request, *args, **kwargs)
        return Response({'success': 'Module Deleted Successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CourseLessonView(viewsets.ModelViewSet):
    """This View is used for Lesson api."""

    queryset = Lesson.objects.all()
    serializer_class = CourseLessonSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create and return success message and adjust the lesson_number accordingly.
        :param request: Lesson data.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().create(request, *args, **kwargs)
        return Response({'success': f'Lesson created successfully.'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        This method is used to update and return success message and adjust the lesson_number accordingly.
        :param request: Lesson data.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
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
        """
        This method is used to destroy and return success message.
        :param request: none.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().destroy(request, *args, **kwargs)
        return Response({'success': 'Lesson Deleted Successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CourseQuestionView(viewsets.ModelViewSet):
    """This View is used for Question api."""

    queryset = Question.objects.all()
    serializer_class = CourseQuestionSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create and return success message.
        :param request: Question data.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().create(request, *args, **kwargs)
        return Response({'success': f'Question created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
        This method is used to destroy and return success message.
        :param request: none.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'Question deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class QuestionOptionsView(viewsets.ModelViewSet):
    """This View is used for QuestionOptions api."""

    queryset = QuestionOptions.objects.all()
    serializer_class = QuestionOptionsSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create and return success message.
        :param request: QuestionOptions data.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().create(request, *args, **kwargs)
        return Response({'success': f'Question Answer created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
        This method is used to destroy and return success message.
        :param request: none.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'Question Answer deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class AssigneeView(viewsets.ModelViewSet):
    """This View is used for Assignee api."""

    queryset = Assignee.objects.all()
    serializer_class = AssigneeSerializer
    pagination_class = AssigneePagination

    @resolve_assignee_name
    def create(self, request, *args, **kwargs):
        """
        This method is used to create and return success message it uses decorator for retrieve the user,
        based on the full_name and designation.
        :param request: Assignee data.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().create(request, *args, **kwargs)
        return Response({'success': f'Assignee created successfully.'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        This method is used to update and return success message.
        :param request: Assignee data.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        return Response({'error': f'Assignee cannot update.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        This method is used to destroy and return success message.
        :param request: none.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'Assignee deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class UserScoreView(viewsets.ModelViewSet):
    """This View is used for User-Score api."""

    queryset = UserScore.objects.all()
    serializer_class = UserScoreSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create and return success message.
        :param request: User Score data.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().create(request, *args, **kwargs)
        return Response({'success': f'User Score created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
        This method is used to destroy and return success message.
        :param request: none.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'User Score deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class UserAnswerView(viewsets.ModelViewSet):
    """This View is used for User-Answer api."""

    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to create and return success message.
        :param request: User Answer data.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().create(request, *args, **kwargs)
        return Response({'success': f'User answer save successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
        This method is used to destroy and return success message.
        :param request: none.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'User answer deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
