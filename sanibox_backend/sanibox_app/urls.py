from django.urls import path
from .views import *

urlpatterns = [
    path("user/session/", user_session_view, name="user-session"),
    #PAGE
    path("index/",index,name='index'),
    path("moviepage/<str:code>/",moviepage,name='moviepage'),
    path("genre/moviepage/",genrewisemoviepage,name='genremoviepage'),

    #API
    path("master/allmovie/",mastermovielistView.as_view(), name="movielist"),
    path('master/genre/',MasterGenreListView.as_view(),name='genrelist'),
    path("master/banner/", MainBannerListView.as_view(), name="main-banner-list"),
    path("master/movie/trending/",TrendingMovieListView.as_view(),name="Movie-Trending-list"),
    path("master/movie/new/",NewMovieListView.as_view(),name="Movie-New-list"),
    path("master/genre/movies/list/",GenreWiseListView.as_view(),name="Genre-Movies-List"),
    path("master/moviespage/<str:movie_code>/",MoviePageListView.as_view(),name="Moviepage-List"),
    path("master/moviespage/<str:movie_code>/casts/",MovieDetailsCastView.as_view(),name="Moviepage-Cast"),
    path("master/moviespage/<str:movie_code>/comments/",MovieCommentsView.as_view(),name="Moviepage-Comment"),
]