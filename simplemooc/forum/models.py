from django.conf import settings
from django.db import models
from django.urls import reverse

from taggit.managers import TaggableManager


# Create your models here.
class Thread(models.Model):
    title = models.CharField('título', max_length=100)
    slug = models.SlugField('identificador', max_length=100, unique=True)
    body = models.TextField('mensagem')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='autor', related_name='threads')
    views = models.PositiveIntegerField('visualizações', default=0, blank=True)
    answers = models.PositiveIntegerField('respostas', default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    class Meta:
        verbose_name = 'tópico'
        verbose_name_plural = 'tópicos'
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:thread', kwargs={'slug': self.slug})


class Reply(models.Model):
    body = models.TextField('resposta')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='autor', related_name='replies')
    thread = models.ForeignKey(Thread, on_delete=models.PROTECT, verbose_name='tópico', related_name='replies')
    correct = models.BooleanField('correta?', default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'resposta'
        verbose_name_plural = 'respostas'
        ordering = ['-correct', 'created_at']

    def __str__(self):
        return self.body[:100]


def post_save_reply(created, instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()
    if instance.correct:
        instance.thread.replies.exclude(pk=instance.pk).update(correct=False)


def post_delete_reply(instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()


models.signals.post_save.connect(post_save_reply, sender=Reply, dispatch_uid='post_save_reply')
models.signals.post_delete.connect(post_delete_reply, sender=Reply, dispatch_uid='post_delete_reply')
