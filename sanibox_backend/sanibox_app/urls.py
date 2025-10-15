from django.urls import path
from .views import *

urlpatterns = [
    path("index/",index,name='index'),
    path("moviepage/<str:code>/",moviepage,name='moviepage'),
    path("master/allmovie/",mastermovielistView.as_view(), name="movielist"),
    path('master/genre/',MasterGenreListView.as_view(),name='genrelist'),
    path("master/banner/", MainBannerListView.as_view(), name="main-banner-list"),
    path("master/movie/trending/",TrendingMovieListView.as_view(),name="Movie-Trending-list"),
    path("master/movie/new/",NewMovieListView.as_view(),name="Movie-New-list"),
]