from django.urls import path
from .views import *

urlpatterns = [
    path("index/",index,name='index'),
    path("moviepage/",moviepage,name='moviepage'),
    path("movielist/",mastermovielistView.as_view(), name="movielist"),
]