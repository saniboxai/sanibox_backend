from datetime import date
from rest_framework import serializers
from .models import *



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
    
class GenreMovieItemSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    maturity_rating = serializers.SerializerMethodField()
    total_episodes_duration = serializers.SerializerMethodField()
    movie_description = serializers.SerializerMethodField()
    main_heros_image = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

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
            "movie_description",
            "main_heros_image",
        ]

    # --- Capitalize every text field ---
    def get_title(self, obj):
        return obj.movie_title.title() if obj.movie_title else None

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

    def get_movie_description(self, obj):
        if obj.movie_description:
            text = obj.movie_description.strip().title()
            words = text.split()
            return " ".join(words[:15]) + ("..." if len(words) > 15 else "")
        return None

    def get_main_heros_image(self, obj):
        details = MasterMovieDetails.objects.filter(master_movie=obj).first()
        if details and details.main_heros:
            return details.main_heros.image  # Only image, not name
        return None


class GenreWiseGroupedSerializer(serializers.Serializer):
    def to_representation(self, queryset):
        grouped_data = {}

        for movie in queryset:
            for genre in movie.genre.all():
                genre_name = genre.category_name.title()
                if genre_name not in grouped_data:
                    grouped_data[genre_name] = []

                grouped_data[genre_name].append({
                    "title": movie.movie_title.title(),
                    "thumbnail_image": movie.thumbnail_image,
                    "like": movie.like,
                    "views": movie.views,
                    "year": movie.release_date.year if movie.release_date else None,
                    "maturity_rating": movie.maturity_rating.rating.title() if movie.maturity_rating else None,
                    "total_episodes_duration": (
                        MasterEpisodes.objects.filter(master_movie=movie)
                        .aggregate(total=models.Sum("total_episodes_duration"))["total"] or 0
                    ),
                    "movie_description": " ".join(movie.movie_description.split()[:15]) + (
                        "..." if len(movie.movie_description.split()) > 15 else ""
                    ) if movie.movie_description else None,
                    "main_heros_image": (
                        MasterMovieDetails.objects.filter(master_movie=movie).first().main_heros.image
                        if MasterMovieDetails.objects.filter(master_movie=movie).exists()
                        else None
                    ),
                    "movie_code": movie.movie_code,
                })

        return grouped_data
    


class MasterEpisodesSerializer(TitleCaseSerializer):
    titlecase_fields = ["episodes_title", "episodes_description"]
    class Meta:
        model = MasterEpisodes
        fields = ['episodes_order', 'episodes_title', 'episodes_description','main_source', 'thumbnail_image', 'release_date', 'is_released']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     for key, value in data.items():
    #         if isinstance(value, str):
    #             data[key] = value.title()
    #     return data


class MasterMovieDetailsSerializer(serializers.ModelSerializer):
    main_heros_image = serializers.SerializerMethodField()
    main_director_name = serializers.SerializerMethodField()
    cast_images = serializers.SerializerMethodField()

    class Meta:
        model = MasterMovieDetails
        fields = ['main_heros_image', 'main_director_name', 'cast_images']

    def get_main_heros_image(self, obj):
        return obj.main_heros.image if obj.main_heros else None

    def get_main_director_name(self, obj):
        return obj.main_director.director_name.title() if obj.main_director else None

    def get_cast_images(self, obj):
        return [cast.image for cast in obj.cast.all() if cast.image]


class MasterMovieSerializer(TitleCaseSerializer):
    titlecase_fields = ["movie_title", "movie_description", "maturity_rating"]

    movie_details = serializers.SerializerMethodField()
    episodes = serializers.SerializerMethodField()
    maturity_rating = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    total_episodes_duration = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = MasterMovie
        fields = [
            'movie_code', 'movie_title', 'movie_description', 'thumbnail_image',
            'main_movie_banner_image', 'movie_trailer', "maturity_rating","age",'like', 'views',
            'release_date', 'is_released','language',"total_episodes_duration",
            'movie_details', 'episodes',
        ]


    def get_maturity_rating(self,obj):
        return obj.maturity_rating.rating.title() if obj.maturity_rating else None
    
    def get_language(self,obj):
        return [l.language.title() for l in obj.language.all()] if obj else []

    def get_movie_details(self, obj):
        details = MasterMovieDetails.objects.filter(master_movie=obj).first()
        return MasterMovieDetailsSerializer(details).data if details else None

    def get_episodes(self, obj):
        eps = MasterEpisodes.objects.filter(master_movie=obj).order_by('episodes_order')
        return MasterEpisodesSerializer(eps, many=True).data
    
    def get_total_episodes_duration(self, obj):
        total = (
            MasterEpisodes.objects.filter(master_movie=obj)
            .aggregate(total=models.Sum("total_episodes_duration"))["total"]
            or 0
        )
        return total or None
    
    def get_age(self,obj):
        return obj.maturity_rating.age if obj.maturity_rating else None

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     for key, value in data.items():
    #         if isinstance(value, str):
    #             data[key] = value.title()
    #     return data


# CAST & DIRECTOR SERIALIZERS

class MasterCastSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterCast
        fields = ["cast_code", "cast_name", "image"]


class MasterDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterDirector
        fields = ["director_code", "director_name", "image"]


class MasterHeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterHeros
        fields = ["hero_code", "hero_name", "image"]


class MasterMovieDetailsSerializer(serializers.ModelSerializer):
    main_heros = MasterHeroSerializer()
    main_director = MasterDirectorSerializer()
    cast = MasterCastSerializer(many=True)

    class Meta:
        model = MasterMovieDetails
        fields = ["main_heros", "main_director", "cast"]


# USER COMMENT SERIALIZERS 

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user", "profile_photo"]

    def to_representation(self, instance):
        return {
            "username": instance.user.username,
            "profile_photo": instance.profile_photo or None
        }


class UserCommentsSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = UserComments
        fields = ["usercommentscode", "user", "user_comments", "created_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["time_ago"] = instance.created_at.strftime("%b %d, %Y")  # you can change to relative time later
        return data