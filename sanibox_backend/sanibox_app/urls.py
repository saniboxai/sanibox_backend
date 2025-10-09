from django.urls import path
from .views import *

urlpatterns = [
    path("movielist",mastermovielistView.as_view(), name="movielist"),
]