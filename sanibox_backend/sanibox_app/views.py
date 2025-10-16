from datetime import timedelta
from django.shortcuts import render,get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView 
from .serializers import *
from .models import *
from django.http import JsonResponse
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request,'index.html')

def moviepage(request, code):
    movie = get_object_or_404(MasterMovie, movie_code=code)
    return render(request, 'movie_page.html', {'movie': movie})

def genrewisemoviepage(request):
    return render(request,'genrewisemovies.html')


def user_session_view(request):
    user = request.user
    if user.is_authenticated:
        avatar = None
        try:
            social = SocialAccount.objects.get(user=user)
            avatar = social.extra_data.get("picture")
        except SocialAccount.DoesNotExist:
            pass
        return JsonResponse({
            "is_authenticated": True,
            "username": user.username,
            "email": user.email,
            "avatar": avatar,
        })
    return JsonResponse({"is_authenticated": False})

class mastermovielistView(generics.ListAPIView):
    serializer_class = MasterMovieSerializer


    def get_queryset(self):
        queryset = MasterMovie.objects.all()
        return queryset
    
    def list(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many=True,context={'request':request})
        if serializer.data:
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        return Response({"data":"Data Not Found"},status=status.HTTP_404_NOT_FOUND)
    

class MasterGenreListView(generics.ListAPIView):
    serializer_class = MasterGenreSerializer

    def get_queryset(self):
        queryset = Genre.objects.all()
        return queryset
    
    def list(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many = True,context = {'request':request})
        if serializer.data:
            return Response({"data":serializer.data},status = status.HTTP_200_OK)
        return Response({"data":"Data Not Found"},status=status.HTTP_404_NOT_FOUND)
    

class MainBannerListView(generics.ListAPIView):

    serializer_class = MainBannerSerializer

    def get_queryset(self):
        return MainBannerImage.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        
        if serializer.data:
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"data": "Data Not Found"}, status=status.HTTP_404_NOT_FOUND)
    

class TrendingMovieListView(generics.ListAPIView):
    serializer_class = TrendingMovieSerializer

    def get_queryset(self):
        # Calculate the weighted score in DB query using annotation
        queryset = (
            MasterMovie.objects.filter(is_released=True)
            .annotate(trending_score=models.F("like") * 0.7 + models.F("views") * 0.3)
            .order_by("-trending_score")[:10]  # top 10 trending
        )
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        
        if serializer.data:
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"data": "Data Not Found"}, status=status.HTTP_404_NOT_FOUND)
    

class NewMovieListView(generics.ListAPIView):
    serializer_class = NewMovieSerializer

    def get_queryset(self):
        recent_days = 30
        cutoff_date = timezone.now().date() - timedelta(days=recent_days)
        return MasterMovie.objects.filter(
            is_released=True,
            release_date__gte=cutoff_date
        ).order_by('-release_date')[:10]
    
class GenreWiseListView(generics.ListAPIView):
    serializer_class = GenreWiseGroupedSerializer

    def get_queryset(self):
        return MasterMovie.objects.filter(is_released=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"data": "Data Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer()
        grouped_data = serializer.to_representation(queryset)
        return Response({"data": grouped_data}, status=status.HTTP_200_OK)
    
class MoviePageListView(generics.RetrieveAPIView):
    serializer_class = MasterMovieSerializer
    lookup_field = 'movie_code'

    def get_queryset(self):
        return MasterMovie.objects.filter(is_released=True)

    def retrieve(self, request, *args, **kwargs):
        movie_code = kwargs.get("movie_code")
        movie = get_object_or_404(self.get_queryset(), movie_code=movie_code)

        serializer = self.get_serializer(movie)
        data = serializer.data

        if not data:
            return Response({"data": "Data Not Found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"data": data}, status=status.HTTP_200_OK)
    

class MovieDetailsCastView(generics.RetrieveAPIView):
    serializer_class = MasterMovieDetailsSerializer
    lookup_field = "master_movie__movie_code"

    def get_queryset(self):
        return MasterMovieDetails.objects.select_related("main_heros", "main_director").prefetch_related("cast")

    def retrieve(self, request, *args, **kwargs):
        movie_code = kwargs.get("movie_code")
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, master_movie__movie_code=movie_code)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class MovieCommentsView(generics.ListAPIView):
    serializer_class = UserCommentsSerializer

    def get_queryset(self):
        movie_code = self.kwargs.get("movie_code")
        movie = get_object_or_404(MasterMovie, movie_code=movie_code)
        return UserComments.objects.filter(user_movie=movie).select_related("user").order_by("-created_at")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No comments found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

