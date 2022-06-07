import json

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, View
from django.http import JsonResponse
from .forms import ReplyForm
from .models import Reply, Thread


# Create your views here.
class ForumView(ListView):
    paginate_by = 10
    template_name = 'forum/index.html'

    def get_queryset(self):
        queryset = Thread.objects.all()
        if 'order' in self.request.GET:
            order = self.request.GET.get('order', '')
            if order == 'views':
                queryset = queryset.order_by('-views')
            elif order == 'answers':
                queryset = queryset.order_by('-answers')

        tag = self.kwargs.get('tag', '')
        if tag:
            queryset = queryset.filter(tags__slug__icontains=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        return context


class ThreadView(DetailView):
    model = Thread
    template_name = 'forum/thread.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.request.user.is_authenticated or self.object.author != self.request.user:
            self.object.views += 1
            self.object.save()
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        context['form'] = ReplyForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Você deve estar logado para responder ao tópico.')
            return redirect(self.request.path)

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = context['form']
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = self.object
            reply.author = self.request.user
            reply.save()
            messages.success(self.request, 'Sua resposta foi enviada com sucesso!')
            context['form'] = ReplyForm()
        return self.render_to_response(context)


class ReplyCorrectView(View):

    correct = True

    def get(self, request, pk):
        reply = get_object_or_404(Reply, pk=pk, thread__author=request.user)
        reply.correct = not reply.correct
        reply.save()
        message = 'Resposta atualizada com sucesso!'
        if request.is_ajax():
            data = {'success': True, 'message': message}
            return JsonResponse(data)
        messages.success(self.request, message)
        return redirect(reply.thread.get_absolute_url())
