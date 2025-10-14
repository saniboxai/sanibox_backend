from rest_framework import serializers
from .models import *

class MasterMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterMovie
        fields = "__all__"

class MasterGenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = ["category_code","category_name"]