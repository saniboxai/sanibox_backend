from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils.text import slugify


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class MainBannerImage(BaseModel):
    ORDER_CHOICES = [(i, str(i)) for i in range(1, 4)]
    banner_code = models.CharField(max_length=50, unique=True, editable=False)
    order_no = models.IntegerField(choices=ORDER_CHOICES)
    image = models.URLField()

    def save(self, *args, **kwargs):
        if not self.banner_code:
            self.banner_code = f"BNR-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Banner {self.order_no}"


class MaturityRating(BaseModel):
    rating_code = models.CharField(max_length=50, unique=True, editable=False)
    rating = models.CharField(max_length=10)
    age = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.rating_code:
            self.rating_code = f"RAT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.rating

class Language(BaseModel):
    language_code = models.CharField(max_length=20, unique=True, editable=False)
    language = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.language_code:
            self.language_code = f"LAN-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.language


class Genre(BaseModel):
    category_name = models.CharField(max_length=100)
    category_code = models.CharField(max_length=50, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.category_code:
            self.category_code = f"GEN-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class SubGenre(BaseModel):
    main_genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="subgenres")
    sub_genre = models.CharField(max_length=100)
    sub_genre_code = models.CharField(max_length=50, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.sub_genre_code:
            self.sub_genre_code = f"SUBG-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sub_genre} ({self.main_genre})"


class MasterDirector(BaseModel):
    director_code = models.CharField(max_length=50, unique=True, editable=False)
    director_name = models.CharField(max_length=100)
    image = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.director_code:
            self.director_code = f"DIR-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.director_name


class MasterHeros(BaseModel):
    hero_code = models.CharField(max_length=50, unique=True, editable=False)
    hero_name = models.CharField(max_length=100)
    image = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.hero_code:
            self.hero_code = f"HRO-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.hero_name


class MasterCast(BaseModel):
    cast_code = models.CharField(max_length=50, unique=True, editable=False)
    cast_name = models.CharField(max_length=100)
    image = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.cast_code:
            self.cast_code = f"CST-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cast_name


class MasterMovie(BaseModel):
    maturity_rating = models.ForeignKey(MaturityRating, on_delete=models.CASCADE)
    language = models.ManyToManyField(Language, blank=True)
    genre = models.ManyToManyField(Genre)
    sub_genre = models.ManyToManyField(SubGenre, blank=True)
    movie_code = models.CharField(max_length=50, unique=True, editable=False)
    movie_title = models.CharField(max_length=200)
    movie_description = models.TextField()
    thumbnail_image = models.URLField()
    main_movie_banner_image = models.URLField()
    movie_trailer = models.URLField(blank=True, null=True)
    like = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.movie_code:
            self.movie_code = f"MOV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.movie_title


class MasterMovieDetails(BaseModel):
    master_movie = models.ForeignKey(MasterMovie, on_delete=models.CASCADE)
    main_heros = models.ForeignKey(MasterHeros, on_delete=models.CASCADE)
    main_director = models.ForeignKey(MasterDirector, on_delete=models.CASCADE)
    cast = models.ManyToManyField(MasterCast, blank=True)
    master_movie_details_code = models.CharField(max_length=50, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.master_movie_details_code:
            self.master_movie_details_code = f"MOVD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.master_movie.movie_title} Details"



class MasterEpisodes(BaseModel):
    master_movie = models.ForeignKey(MasterMovie, on_delete=models.CASCADE)
    episodes_order = models.PositiveSmallIntegerField()
    episodes_title = models.CharField(max_length=200)
    episodes_description = models.TextField()
    thumbnail_image = models.URLField()
    main_source = models.URLField()
    views = models.PositiveIntegerField(default=0)
    episodes_code = models.CharField(max_length=50, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.episodes_code:
            self.episodes_code = f"EPS-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.master_movie.movie_title} - Ep {self.episodes_order}"

class UserProfile(BaseModel):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    profile_photo = models.URLField(blank=True, null=True)
    language_pref = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    genre_pref = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    sensitive_content = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Watchlist(BaseModel):
    watchlist_code = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    watchlist_name = models.CharField(max_length=100)
    user_movie = models.ForeignKey(MasterMovie, on_delete=models.CASCADE, null=True, blank=True)
    user_episodes = models.ForeignKey(MasterEpisodes, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.watchlist_code:
            self.watchlist_code = f"WCH-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.watchlist_name}"
