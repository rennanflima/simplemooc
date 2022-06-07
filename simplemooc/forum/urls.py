from django.urls import path

from simplemooc.forum.views import ForumView, ReplyCorrectView, ThreadView

app_name = 'forum'
urlpatterns = [
    path('', ForumView.as_view(), name='index'),
    path('tag/<slug:tag>/', ForumView.as_view(), name='index_tagged'),
    path('topico/<slug:slug>/', ThreadView.as_view(), name='thread'),
    path('respostas/<int:pk>/correta', ReplyCorrectView.as_view(), name='reply_correct'),
    path('respostas/<int:pk>/incorreta', ReplyCorrectView.as_view(correct=False), name='reply_incorrect'),
]
