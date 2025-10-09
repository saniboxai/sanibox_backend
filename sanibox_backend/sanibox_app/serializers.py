from rest_framework import serializers
from .models import *

class MasterMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterMovie
        fields = ["*"]
