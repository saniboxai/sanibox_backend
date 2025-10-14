from rest_framework import serializers
from .models import *

class MasterMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterMovie
        fields = "__all__"

class MasterGenreSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ["category_code", "category_name"]

    def get_category_name(self, obj):
        return obj.category_name.capitalize() if obj.category_name else ""