from course.models import (
    CourseCategory,
    Course,
    Module,
)
from rest_framework import viewsets
from ..serializers.course_serializer import (
    CourseCategorySerializer,
    CourseSerializer,
    ModuleSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F


class CourseCategoryView(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'Category created successfully.'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response({'error': f'Category cannot update.'}, status=status.HTTP_204_NO_CONTENT)

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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            course = serializer.validated_data['course']
            module_number = serializer.validated_data['module_number']
            if Module.objects.filter(course=course, module_number=module_number).exists():
                Module.objects.filter(course=course, module_number__gte=module_number).update(
                                        module_number=F('module_number') + 1)
            serializer.save()
            return Response({'success': 'Module Created Successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def partial_update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #
    #     if serializer.is_valid():
    #         if 'module_number' in serializer.validated_data:
    #             Module.objects.filter(course=instance.course, module_number__gte=serializer.validated_data['module_number']).update(module_number=F('module_number')+1)
    #         serializer.save()
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        Module.objects.filter(course=instance.course, module_number__gte=instance.module_number).update(
            module_number=F('module_number') - 1)
        instance.delete()
        return Response({'success': 'Module Deleted Successfully.'}, status=status.HTTP_204_NO_CONTENT)
