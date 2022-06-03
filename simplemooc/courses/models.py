from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.
class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query)
        )


class Course(models.Model):
    name = models.CharField('nome', max_length=100)
    slug = models.SlugField('atalho')
    description = models.TextField('descrição simples', blank=True)
    about = models.TextField('sobre o curso', blank=True)
    start_date = models.DateField('data de início', null=True, blank=True)
    image = models.ImageField('imagem', upload_to='courses/images', null=True, blank=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    objects = CourseManager()

    class Meta:
        verbose_name = 'curso'
        verbose_name_plural = 'cursos'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courses:details', kwargs={'slug': self.slug})


class Enrollment(models.Model):
    PENDENTE = 'PENDENTE'
    APROVADO = 'APROVADO'
    CANCELADO = 'CANCELADO'
    STATUS_CHOICES = (
        (PENDENTE, 'Pendente'),
        (APROVADO, 'Aprovado'),
        (CANCELADO, 'Cancelado'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='usuário', related_name='enrollments')
    course = models.ForeignKey('courses.Course', on_delete=models.PROTECT, verbose_name='curso', related_name='enrollments')
    status = models.CharField('situação', max_length=30, choices=STATUS_CHOICES, default=PENDENTE, blank=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'inscrição'
        verbose_name_plural = 'inscrições'
        unique_together = (('user', 'course'),)

    def active(self):
        self.status = self.APROVADO
        self.save()

    def is_approved(self):
        return self.status == self.APROVADO


class Announcement(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.PROTECT, verbose_name='curso', related_name='announcements')
    title = models.CharField('título', max_length=100)
    content = models.TextField('conteúdo')
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'anúncio'
        verbose_name_plural = 'anúncios'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    announcement = models.ForeignKey('courses.Announcement', on_delete=models.PROTECT, verbose_name='anúncio', related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='usuário', related_name='comments')
    comment = models.TextField('comentário')
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'comentário'
        verbose_name_plural = 'comentários'
        ordering = ['created_at']

    def __str__(self):
        return self.comment


def post_save_announcement(instance, created, **kwargs):
    if created:
        from simplemooc.core.mail import send_mail_template
        subject = instance.title
        context = {
            'announcement': instance
        }
        template_name = 'courses/announcement_mail.html'
        enrollments = instance.course.enrollments.filter(status=Enrollment.APROVADO)
        for enrollment in enrollments:
            recipient = [enrollment.user.email]
            send_mail_template(subject, template_name, context, recipient)


models.signals.post_save.connect(post_save_announcement, sender=Announcement, dispatch_uid='post_save_announcement')
