from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView 
from .serializers import *
from .models import *
# Create your views here.


def index(request):
    return render(request,'index.html')

def moviepage(request):
    return render(request,'movie_page.html')

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