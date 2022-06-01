from django.urls import path
from simplemooc.core.views import contact, home

app_name = 'core'
urlpatterns = [
    path('', home, name='home'),
    path('contato/', contact, name='contact'),
]
