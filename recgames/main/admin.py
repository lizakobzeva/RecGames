from django.contrib import admin
from .models import Tag, Game, Collection, GameCollection, Recommendation, Favorite, UserProfile, Feedback, CollectionLike

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'developer', 'release_year', 'platforms', 'rating', 'price', 'created_at')
    list_filter = ('genre', 'platforms', 'release_year', 'created_at')
    search_fields = ('title', 'developer', 'description')
    filter_horizontal = ('tags',)
    list_editable = ('price', 'rating')
    list_per_page = 25
    ordering = ('-created_at',)
    
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'genre', 'developer', 'release_year', 'platforms')
        }),
        ('Детали игры', {
            'fields': ('price', 'rating', 'description')
        }),
        ('Медиа и ссылки', {
            'fields': ('game_image', 'steam_url'),
            'classes': ('collapse',)
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
        ('Теги', {
            'fields': ('tags',) 
        }),
    )
    
    readonly_fields = ('created_at',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  
            return self.readonly_fields + ('created_at',)
        return self.readonly_fields
    

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_public', 'games_count', 'likes_count', 'created_at')
    list_filter = ('is_public', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'user__username')
    list_editable = ('is_public',)
    list_per_page = 25
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'title', 'description', 'is_public')
        }),
        ('Статистика', {
            'fields': ('likes_count',),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at', 'games_count')
    
    actions = ['make_public', 'make_private', 'reset_likes']
    
    def make_public(self, request, queryset):
        updated = queryset.update(is_public=True)
        self.message_user(request, f'{updated} подборок стали публичными')
    make_public.short_description = "Сделать выбранные подборки публичными"
    
    def make_private(self, request, queryset):
        updated = queryset.update(is_public=False)
        self.message_user(request, f'{updated} подборок стали приватными')
    make_private.short_description = "Сделать выбранные подборки приватными"
    
    def reset_likes(self, request, queryset):
        updated = queryset.update(likes_count=0)
        self.message_user(request, f'Лайки сброшены для {updated} подборок')
    reset_likes.short_description = "Сбросить лайки у выбранных подборок"
    
    def games_count(self, obj):
        return obj.games.count()
    games_count.short_description = 'Количество игр'

@admin.register(GameCollection)
class GameCollectionAdmin(admin.ModelAdmin):
    list_display = ('game', 'collection', 'order', 'added_at')
    list_filter = ('added_at', 'collection')
    search_fields = ('game__title', 'collection__title')
    list_editable = ('order',)
    list_per_page = 25
    ordering = ('collection', 'order')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('collection', 'game', 'order')
        }),
        ('Системная информация', {
            'fields': ('added_at',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('added_at',)
    
    actions = ['reorder_games']
    
    def reorder_games(self, request, queryset):
        for collection in Collection.objects.all():
            games_in_collection = GameCollection.objects.filter(collection=collection)
            for index, game_collection in enumerate(games_in_collection):
                game_collection.order = index + 1
                game_collection.save()
        self.message_user(request, 'Порядок игр во всех подборках пересчитан')
    reorder_games.short_description = "Пересчитать порядок игр в подборках"

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'parameters_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'game__title')
    list_per_page = 25
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'game')
        }),
        ('Параметры рекомендации', {
            'fields': ('parameters',),
            'classes': ('collapse',)
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at',)
    
    def parameters_preview(self, obj):
        params = str(obj.parameters)[:50]
        return params + '...' if len(str(obj.parameters)) > 50 else params
    parameters_preview.short_description = 'Параметры'

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'game__title')
    list_per_page = 25
    ordering = ('-added_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'game')
        }),
        ('Системная информация', {
            'fields': ('added_at',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('added_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferences_count', 'collections_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')
    list_per_page = 25
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user',)
        }),
        ('Предпочтения', {
            'fields': ('preferences',),
            'classes': ('collapse',)
        }),
        ('Статистика', {
            'fields': ('collections_count',)
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'preferences_count')
    
    actions = ['reset_collections_count']
    
    def reset_collections_count(self, request, queryset):
        for profile in queryset:
            actual_count = Collection.objects.filter(user=profile.user).count()
            profile.collections_count = actual_count
            profile.save()
        self.message_user(request, 'Количество подборок пересчитано для выбранных профилей')
    reset_collections_count.short_description = "Пересчитать количество подборок"
    
    def preferences_count(self, obj):
        return len(obj.preferences)
    preferences_count.short_description = 'Количество предпочтений'

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_processed') 
    list_filter = ('is_processed', 'created_at') 
    search_fields = ('name', 'email', 'message') 
    list_editable = ('is_processed',) 
    readonly_fields = ('created_at',) 

@admin.register(CollectionLike)
class CollectionLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'collection', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'collection__title')
    list_per_page = 25
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'collection')
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at',)