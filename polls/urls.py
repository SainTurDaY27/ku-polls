"""This urls.py contain path for polls."""
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', login_required(views.DetailView.as_view()), name='detail'),
    path('<int:pk>/results/', views.ResultView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
