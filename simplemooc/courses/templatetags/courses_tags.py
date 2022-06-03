from django import template

register = template.Library()


@register.inclusion_tag('courses/templatetags/my_courses.html')
def my_courses(user):
    enrollments = user.enrollments.all()
    context = {
        'enrollments': enrollments
    }
    return context


@register.simple_tag
def load_my_courses(user):
    return user.enrollments.all()
