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
