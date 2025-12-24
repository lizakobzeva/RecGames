from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Тег')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL-имя')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

class Game(models.Model):
    GENRE_CHOICES = [
        ('RPG', 'RPG'),
        ('Adventure', 'Adventure'),
        ('Puzzle', 'Puzzle'),
        ('Action', 'Action'),
        ('Strategy', 'Strategy'),
        ('Simulation', 'Simulation'),
        ('Sports', 'Sports'),
        ('Racing', 'Racing'),
        ('Horror', 'Horror'),
        ('FPS', 'First-Person Shooter'),
        ('MMO', 'Massively Multiplayer Online'),
        ('Visual Novel', 'Visual Novel'),
        ('Metroidvania', 'Metroidvania'),
        ('Roguelike', 'Roguelike'),
        ('Tactical Shooter', 'Tactical Shooter'),
        ('Survival', 'Survival'),
        ('Shooter', 'Shooter'),
        ('Sandbox', 'Sandbox'),
    ]
    
    PLATFORM_CHOICES = [
        ('PC', 'PC'),
        ('PlayStation', 'PlayStation'),
        ('Xbox', 'Xbox'),
        ('Nintendo Switch', 'Nintendo Switch'),
        ('Mobile', 'Mobile'),
        ('Multiplatform', 'Multiplatform'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название игры')
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, verbose_name='Жанр')
    developer = models.CharField(max_length=200, verbose_name='Разработчик')
    release_year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[
            MinValueValidator(1970),
            MaxValueValidator(2030)
        ]
    )
    price = models.IntegerField(
        verbose_name='Цена',
        validators=[MinValueValidator(0)]
    )
    platforms = models.CharField(max_length=50, choices=PLATFORM_CHOICES, verbose_name='Платформы')
    rating = models.IntegerField( 
        verbose_name='Рейтинг (0-10)',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    description = models.TextField(verbose_name='Описание игры')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги для рекомендаций')    
    game_image = models.URLField(verbose_name='Обложка игры')
    steam_url = models.URLField(verbose_name='Ссылка на Steam')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['-created_at']

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель подборки')
    title = models.CharField(max_length=200, verbose_name='Название подборки')
    description = models.TextField(verbose_name='Описание подборки')
    games = models.ManyToManyField('Game', through='GameCollection', related_name='collections')
    is_public = models.BooleanField(default=True, verbose_name='Публичная подборка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    likes_count = models.IntegerField(default=0, verbose_name='Количество лайков')
    
    def __str__(self):
        return f"{self.title} от {self.user.username}"
    
    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'
        ordering = ['-created_at']

class GameCollection(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, verbose_name='Подборка')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Игра')
    order = models.IntegerField(default=0, verbose_name='Порядок в подборке')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
    def __str__(self):
        return f"{self.game.title} в {self.collection.title}"
    
    class Meta:
        verbose_name = 'Игра в подборке'
        verbose_name_plural = 'Игры в подборках'
        ordering = ['order']
        unique_together = ['collection', 'game']


class CollectionLike(models.Model):
    """Модель для лайков/избранных подборок"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, verbose_name='Подборка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
    def __str__(self):
        return f"{self.user.username} лайкнул {self.collection.title}"
    
    class Meta:
        verbose_name = 'Лайк подборки'
        verbose_name_plural = 'Лайки подборок'
        unique_together = ['user', 'collection']
        ordering = ['-created_at']

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Рекомендованная игра')
    parameters = models.JSONField(default=dict, verbose_name='Параметры запроса')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата рекомендации')
    
    def __str__(self):
        return f"Рекомендация {self.game.title} для {self.user.username}"
    
    class Meta:
        verbose_name = 'Рекомендация'
        verbose_name_plural = 'Рекомендации'
        ordering = ['-created_at']

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Игра')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
    def __str__(self):
        return f"{self.game.title} в избранном у {self.user.username}"
    
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные игры'
        ordering = ['-added_at']
        unique_together = ['user', 'game']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    preferences = models.JSONField(default=list, verbose_name='Предпочтения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    collections_count = models.IntegerField(default=0, verbose_name='Количество созданных подборок')
    
    def __str__(self):
        return f"Профиль {self.user.username}"
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email') 
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки') 
    is_processed = models.BooleanField(default=False, verbose_name='Обработано') 
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратные связи'
        ordering = ['-created_at']