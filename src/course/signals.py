from django.db.models.signals import pre_save, pre_delete
from .models import Module, Lesson
from django.dispatch import receiver
from django.db.models import F


@receiver(pre_save, sender=Module)
def update_module_number(sender, instance, **kwargs):
    if Module.objects.filter(course=instance.course, module_number=instance.module_number).exists():
        Module.objects.filter(course=instance.course, module_number__gte=instance.module_number).update(
            module_number=F('module_number') + 1)

@receiver(pre_delete, sender=Module)
def adjust_module_number(sender, instance, **kwargs):
    Module.objects.filter(course=instance.course, module_number__gt=instance.module_number).update(
        module_number=F('module_number') - 1)

@receiver(pre_save, sender=Lesson)
def update_lesson_number(sender, instance, **kwargs):
    if Lesson.objects.filter(module=instance.module, lesson_number=instance.lesson_number).exists():
        Lesson.objects.filter(module=instance.module, lesson_number__gte=instance.lesson_number).update(
            lesson_number=F('lesson_number') + 1)

@receiver(pre_delete, sender=Lesson)
def adjust_module_number(sender, instance, **kwargs):
    Lesson.objects.filter(module=instance.module, lesson_number__gte=instance.lesson_number).update(
        lesson_number=F('lesson_number') - 1)
