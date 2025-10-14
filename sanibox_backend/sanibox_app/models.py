from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
import uuid

#BASEMODEL
class BaseModel(models.Model):
    """
    Abstract base model that includes common fields for all models.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(self, field.name, None)
                if isinstance(value, str):
                    setattr(self, field.name, value.lower())
        super().save(*args, **kwargs)


#MASTERDATAMODELS

class MainBannerImage(BaseModel):
    ORDER_CHOICES = [(i, str(i)) for i in range(1, 4)]
    banner_code = models.CharField(max_length=50, unique=True, editable=False)
    order_no = models.IntegerField(choices=ORDER_CHOICES)
    title = models.CharField(max_length=100, blank=True)
    image = models.URLField()

    def save(self, *args, **kwargs):
        if not self.banner_code:
            self.banner_code = f"BNR-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Banner {self.order_no} - {self.title or 'Untitled'}"

    class Meta:
        ordering = ['order_no']


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


#MASTERTABLE

class MasterMovie(BaseModel):
    TYPE_CHOICES = [
        ('MOVIE', 'Movie'),
        ('SERIES', 'Web Series'),
    ]

    maturity_rating = models.ForeignKey(MaturityRating, on_delete=models.CASCADE)
    language = models.ManyToManyField(Language, blank=True)
    genre = models.ManyToManyField(Genre)
    sub_genre = models.ManyToManyField(SubGenre, blank=True)
    movie_code = models.CharField(max_length=50, unique=True, editable=False)
    movie_title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    movie_description = models.TextField()
    thumbnail_image = models.URLField()
    main_movie_banner_image = models.URLField()
    movie_trailer = models.URLField(blank=True, null=True)
    like = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    content_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='MOVIE')
    release_date = models.DateField(null=True, blank=True)
    is_released = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.movie_code:
            self.movie_code = f"MOV-{uuid.uuid4().hex[:8].upper()}"
        if not self.slug:
            self.slug = slugify(self.movie_title)
        super().save(*args, **kwargs)

    @property
    def is_upcoming(self):
        if self.release_date:
            return self.release_date > timezone.now().date()
        return not self.is_released

    @property
    def total_duration(self):
        if self.content_type == 'SERIES':
            return sum((ep.total_episodes_duration for ep in self.masterepisodes_set.all()), timezone.timedelta())
        return None

    def __str__(self):
        return self.movie_title

    class Meta:
        ordering = ['release_date']
        indexes = [models.Index(fields=['release_date', 'movie_title'])]


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
    season_number = models.PositiveSmallIntegerField(default=1)
    episodes_order = models.PositiveSmallIntegerField()
    episodes_title = models.CharField(max_length=200)
    episodes_description = models.TextField()
    thumbnail_image = models.URLField()
    main_source = models.URLField()
    views = models.PositiveIntegerField(default=0)
    episodes_code = models.CharField(max_length=50, unique=True, editable=False)
    total_episodes_duration = models.IntegerField()
    release_date = models.DateTimeField(null=True, blank=True)
    is_released = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.episodes_code:
            self.episodes_code = f"EPS-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def is_upcoming(self):
        if self.release_date:
            return self.release_date > timezone.now()
        return not self.is_released

    @property
    def duration_in_minutes(self):
        return int(self.total_episodes_duration.total_seconds() / 60)

    def __str__(self):
        return f"{self.master_movie.movie_title} - S{self.season_number}E{self.episodes_order}"

    class Meta:
        unique_together = ('master_movie', 'season_number', 'episodes_order')
        ordering = ['season_number', 'episodes_order']

#USERPROFILES
class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.URLField(blank=True, null=True)
    language_pref = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    genre_pref = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    sensitive_content = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Watchlist(BaseModel):
    watchlist_code = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="watchlists")
    watchlist_name = models.CharField(max_length=100)
    user_movie = models.ForeignKey(MasterMovie, on_delete=models.CASCADE, null=True, blank=True)
    user_episodes = models.ForeignKey(MasterEpisodes, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.watchlist_code:
            self.watchlist_code = f"WCH-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.user.username} - {self.watchlist_name}"

    class Meta:
        ordering = ['-created_at']


class UserHistory(BaseModel):
    userhistorycode = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='history')
    user_movie = models.ForeignKey(MasterMovie, on_delete=models.CASCADE, null=True, blank=True)
    user_episodes = models.ForeignKey(MasterEpisodes, on_delete=models.CASCADE, null=True, blank=True)
    user_watching_duration = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.userhistorycode:
            self.userhistorycode = f"UHC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.user.username} - {self.userhistorycode}"


class UserRating(BaseModel):
    userratingcode = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings')
    user_rating = models.IntegerField()
    user_movie = models.ForeignKey(MasterMovie, on_delete=models.CASCADE, null=True, blank=True)
    user_episodes = models.ForeignKey(MasterEpisodes, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.userratingcode:
            self.userratingcode = f"URC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.user.username} - {self.user_rating}/5"


class UserComments(BaseModel):
    usercommentscode = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
    user_comments = models.TextField()
    user_movie = models.ForeignKey(MasterMovie, on_delete=models.CASCADE, null=True, blank=True)
    user_episodes = models.ForeignKey(MasterEpisodes, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.usercommentscode:
            self.usercommentscode = f"UCC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.user.username} - {self.usercommentscode}"
