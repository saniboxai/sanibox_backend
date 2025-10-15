from datetime import date
from rest_framework import serializers
from .models import *

class MasterMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterMovie
        fields = "__all__"


class TitleCaseSerializer(serializers.ModelSerializer):

    titlecase_fields = []

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in self.titlecase_fields:
            value = data.get(field)
            if isinstance(value, str):
                data[field] = value.title()
        return data

class MasterGenreSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ["category_code", "category_name"]

    def get_category_name(self, obj):
        return obj.category_name.capitalize() if obj.category_name else ""
    


class MainBannerSerializer(TitleCaseSerializer):
    titlecase_fields = ["title", "movie_description", "maturity_rating"]

    movie_description = serializers.SerializerMethodField()
    maturity_rating = serializers.SerializerMethodField()
    total_episodes_duration = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    movie_code = serializers.SerializerMethodField()

    class Meta:
        model = MainBannerImage
        fields = [
            "title",
            "image",
            "movie_description",
            "maturity_rating",
            "total_episodes_duration",
            "genre",
            "language",
            "movie_code",
        ]

    def get_movie(self, obj):
        return MasterMovie.objects.filter(movie_title__iexact=obj.title).first()

    def get_movie_description(self, obj):
        movie = self.get_movie(obj)
        return movie.movie_description if movie else None

    def get_maturity_rating(self, obj):
        movie = self.get_movie(obj)
        return movie.maturity_rating.rating if movie and movie.maturity_rating else None

    def get_genre(self, obj):
        movie = self.get_movie(obj)
        return [g.category_name.title() for g in movie.genre.all()] if movie else []

    def get_language(self, obj):
        movie = self.get_movie(obj)
        return [l.language.title() for l in movie.language.all()] if movie else []

    def get_total_episodes_duration(self, obj):
        movie = self.get_movie(obj)
        total = (
            MasterEpisodes.objects.filter(master_movie=movie)
            .aggregate(total=models.Sum("total_episodes_duration"))["total"]
            or 0
        )
        return total or None
    
    def get_movie_code(self,obj):
        movie = self.get_movie(obj)
        return movie.movie_code if movie else None
    

class TrendingMovieSerializer(TitleCaseSerializer):
    titlecase_fields = ["title", "movie_description", "maturity_rating","genre"]

    year = serializers.SerializerMethodField()
    maturity_rating = serializers.SerializerMethodField()
    total_episodes_duration = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    movie_description = serializers.SerializerMethodField()
    main_heros_image = serializers.SerializerMethodField()
    trending_score = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    movie_code = serializers.SerializerMethodField()

    class Meta:
        model = MasterMovie
        fields = [
            "title",
            "thumbnail_image",
            "like",
            "views",
            "year",
            "maturity_rating",
            "total_episodes_duration",
            "genre",
            "movie_description",
            "main_heros_image",
            "trending_score",
            "movie_code",
        ]

    def get_title(self,obj):
        return obj.movie_title if obj.movie_title else None

    def get_year(self, obj):
        return obj.release_date.year if obj.release_date else None

    def get_maturity_rating(self, obj):
        return obj.maturity_rating.rating.title() if obj.maturity_rating else None

    def get_total_episodes_duration(self, obj):
        total = (
            MasterEpisodes.objects.filter(master_movie=obj)
            .aggregate(total=models.Sum("total_episodes_duration"))["total"]
            or 0
        )
        return total or None

    def get_genre(self, obj):
        return [g.category_name.title() for g in obj.genre.all()]

    def get_movie_description(self, obj):
        if obj.movie_description:
            words = obj.movie_description.split()
            return " ".join(words[:15]) + ("..." if len(words) > 15 else "")
        return None

    def get_main_heros_image(self, obj):
        details = MasterMovieDetails.objects.filter(master_movie=obj).first()
        if details and details.main_heros:
            return details.main_heros.image  # assuming field name is hero_image
        return None


    def get_trending_score(self, obj):
        """
        Compute a weighted popularity score.
        Example formula: 70% likes + 30% views.
        """
        return round(obj.like * 0.7 + obj.views * 0.3, 2)
    
    def get_movie_code(self,obj):
        return obj.movie_code if obj.movie_code else None
    

class NewMovieSerializer(TitleCaseSerializer):
    titlecase_fields = ["title", "movie_description", "maturity_rating", "genre"]

    year = serializers.SerializerMethodField()
    maturity_rating = serializers.SerializerMethodField()
    total_episodes_duration = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    movie_description = serializers.SerializerMethodField()
    main_heros_image = serializers.SerializerMethodField()
    days_since_release = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    movie_code = serializers.SerializerMethodField()

    class Meta:
        model = MasterMovie
        fields = [
            "title",
            "thumbnail_image",
            "like",
            "views",
            "year",
            "maturity_rating",
            "total_episodes_duration",
            "genre",
            "movie_description",
            "main_heros_image",
            "days_since_release",
            "movie_code",
        ]

    def get_title(self, obj):
        return obj.movie_title if obj.movie_title else None

    def get_year(self, obj):
        return obj.release_date.year if obj.release_date else None

    def get_maturity_rating(self, obj):
        return obj.maturity_rating.rating.title() if obj.maturity_rating else None

    def get_total_episodes_duration(self, obj):
        total = (
            MasterEpisodes.objects.filter(master_movie=obj)
            .aggregate(total=models.Sum("total_episodes_duration"))["total"]
            or 0
        )
        return total or None

    def get_genre(self, obj):
        return [g.category_name.title() for g in obj.genre.all()]

    def get_movie_description(self, obj):
        if obj.movie_description:
            words = obj.movie_description.split()
            return " ".join(words[:15]) + ("..." if len(words) > 15 else "")
        return None

    def get_main_heros_image(self, obj):
        details = MasterMovieDetails.objects.filter(master_movie=obj).first()
        if details and details.main_heros:
            return details.main_heros.image  # assuming field name is 'image'
        return None

    def get_days_since_release(self, obj):
        """Return how long ago the movie was released (or upcoming)."""
        if obj.release_date:
            today = date.today()
            if obj.release_date > today:
                days = (obj.release_date - today).days
                return f"Releasing in {days} days"
            else:
                days = (today - obj.release_date).days
                if days == 0:
                    return "Released Today"
                elif days == 1:
                    return "Released 1 day ago"
                return f"Released {days} days ago"
        return "Release date unknown"
    
    def get_movie_code(self,obj):
        return obj.movie_code if obj.movie_code else None
    

# class MainMovieSerializer(TitleCaseSerializer):
