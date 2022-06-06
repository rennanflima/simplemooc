import re
from multiprocessing import context

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import enrollment_required
from .forms import CommentForm, ContactCourse
from .models import Course, Enrollment


# Create your views here.
def index(request):
    template_name = 'courses/index.html'
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, template_name, context)


def details(request, slug):
    template_name = 'courses/details.html'
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()

    context['course'] = course
    context['form'] = form
    return render(request, template_name, context)


@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        enrollment.active()
        messages.success(request, 'Você foi inscrito no curso com sucesso.')
    else:
        messages.info(request, 'Você já está inscrito no curso.')

    return redirect('accounts:dashboard')


@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(request.user.enrollments.all(), course=course)
    template_name = 'courses/undo_enrollment.html'
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso.')
        return redirect('accounts:dashboard')
    context = {
        'course': course,
        'enrollment': enrollment,
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def announcements(request, slug):
    template_name = 'courses/announcements.html'
    course = request.course

    context = {
        'course': course,
        'announcements': course.announcements.all(),
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    template_name = 'courses/show_announcement.html'
    course = request.course

    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, 'Seu comentário foi enviado com sucesso.')
    context = {
        'course': course,
        'announcement': announcement,
        'form': form,
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def lessons(request, slug):
    template_name = 'courses/lessons.html'
    course = request.course

    if request.user.is_staff:
        lessons = course.lessons.all()
    else:
        lessons = course.release_lessons()

    context = {
        'course': course,
        'lessons': lessons,
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def show_lesson(request, slug, pk):
    template_name = 'courses/show_lesson.html'
    course = request.course
    lesson = get_object_or_404(course.lessons.all(), pk=pk)

    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Esta aula não está disponível para você.')
        return redirect('courses:lessons', slug=course.slug)

    context = {
        'course': course,
        'lesson': lesson,
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def material(request, slug, lesson_id, pk):
    template_name = 'courses/material.html'
    course = request.course
    lesson = get_object_or_404(course.lessons.all(), pk=lesson_id)

    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Esta aula não está disponível para você.')
        return redirect('courses:lessons', slug=course.slug)

    material = get_object_or_404(lesson.materials.all(), pk=pk)

    if not material.is_embedded:
        return redirect(material.file.url)

    context = {
        'course': course,
        'lesson': lesson,
        'material': material,
    }
    return render(request, template_name, context)
