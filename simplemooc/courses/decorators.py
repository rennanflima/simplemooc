from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .models import Course, Enrollment


def enrollment_required(view_func):
    def _wrapper(request, *args, **kwargs):
        slug = kwargs.get('slug')
        course = get_object_or_404(Course, slug=slug)
        has_permission = request.user.is_staff
        if not has_permission:
            try:
                enrollment = request.user.enrollments.filter(course=course)[0:1].get()
            except Enrollment.DoesNotExist:
                message = 'Desculpe, você não tem permissão para acessar este curso.'
            else:
                if enrollment.is_approved():
                    has_permission = True
                else:
                    message = 'A sua inscrição ainda está pendente.'

        if not has_permission:
            messages.error(request, message)
            return redirect('accounts:dashboard')

        request.course = course
        return view_func(request, *args, **kwargs)
    return _wrapper
