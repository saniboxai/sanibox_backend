from django.urls import path
from .views import *

urlpatterns = [
    path("index/",index,name='index'),
    path("moviepage/",moviepage,name='moviepage'),
    path("movielist/",mastermovielistView.as_view(), name="movielist"),
    path('genrelist/',MasterGenreListView.as_view(),name='genrelist'),
]