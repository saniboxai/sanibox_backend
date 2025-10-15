from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *


@admin.register(MainBannerImage)
class MainBannerImageAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'title', 'banner_code', 'image')
    ordering = ('order_no',)
    search_fields = ('title',)


@admin.register(MaturityRating)
class MaturityRatingAdmin(admin.ModelAdmin):
    list_display = ('rating', 'age', 'rating_code')
    search_fields = ('rating',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language', 'language_code')
    search_fields = ('language',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_code')
    search_fields = ('category_name',)


@admin.register(SubGenre)
class SubGenreAdmin(admin.ModelAdmin):
    list_display = ('sub_genre', 'main_genre', 'sub_genre_code')
    search_fields = ('sub_genre', 'main_genre__category_name')


@admin.register(MasterDirector)
class MasterDirectorAdmin(admin.ModelAdmin):
    list_display = ('director_name', 'director_code')
    search_fields = ('director_name',)


@admin.register(MasterHeros)
class MasterHerosAdmin(admin.ModelAdmin):
    list_display = ('hero_name', 'hero_code')
    search_fields = ('hero_name',)


@admin.register(MasterCast)
class MasterCastAdmin(admin.ModelAdmin):
    list_display = ('cast_name', 'cast_code')
    search_fields = ('cast_name',)


class MasterEpisodesInline(admin.TabularInline):
    model = MasterEpisodes
    extra = 0
    fields = (
        'season_number',
        'episodes_order',
        'episodes_title',
        'release_date',
        'is_released',
        'thumbnail_image',
        'main_source',
        'total_episodes_duration',
        'views',
    )
    readonly_fields = ('episodes_code', 'views')
    ordering = ('season_number', 'episodes_order')


@admin.register(MasterMovie)
class MasterMovieAdmin(admin.ModelAdmin):
    list_display = (
        'movie_title',
        'content_type',
        'release_date',
        'is_released',
        'like',
        'views',
    )
    list_filter = ('content_type', 'is_released', 'release_date', 'genre')
    search_fields = ('movie_title', 'movie_code')
    ordering = ('-release_date',)
    inlines = [MasterEpisodesInline]
    filter_horizontal = ('language', 'genre', 'sub_genre')
    readonly_fields = ('slug',) 


@admin.register(MasterMovieDetails)
class MasterMovieDetailsAdmin(admin.ModelAdmin):
    list_display = ('master_movie', 'main_director', 'main_heros', 'master_movie_details_code')
    filter_horizontal = ('cast',)


@admin.register(MasterEpisodes)
class MasterEpisodesAdmin(admin.ModelAdmin):
    list_display = ('episodes_title', 'master_movie', 'season_number', 'episodes_order', 'release_date', 'is_released', 'views')
    list_filter = ('is_released', 'release_date', 'master_movie')
    search_fields = ('episodes_title', 'master_movie__movie_title')
    ordering = ('master_movie', 'season_number', 'episodes_order')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'language_pref', 'genre_pref', 'sensitive_content')
    search_fields = ('user__username', 'user__email')


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'watchlist_name', 'user_movie', 'user_episodes', 'watchlist_code')
    search_fields = ('user__user__username', 'watchlist_name')


@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_movie', 'user_episodes', 'user_watching_duration', 'userhistorycode')
    search_fields = ('user__user__username', 'user_movie__movie_title', 'user_episodes__episodes_title')


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_rating', 'user_movie', 'user_episodes', 'userratingcode')
    list_filter = ('user_rating',)
    search_fields = ('user__user__username', 'user_movie__movie_title', 'user_episodes__episodes_title')


@admin.register(UserComments)
class UserCommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_movie', 'user_episodes', 'usercommentscode')
    search_fields = ('user__user__username', 'user_comments')
