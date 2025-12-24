from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.db.models import Q, Count
import json
from .models import Game, Collection, Feedback, Tag, Favorite, GameCollection, CollectionLike
from .forms import FeedbackForm, CollectionForm, AddGameToCollectionForm
from .reg_forms import CustomUserCreationForm  

def home(request):
    latest_games = Game.objects.all().order_by('-created_at')[:8]
    popular_collections = Collection.objects.filter(is_public=True).annotate(
        like_count=Count('collectionlike')
    ).order_by('-like_count', '-created_at')[:6]
    
    favorite_game_ids = []
    if request.user.is_authenticated:
        favorite_game_ids = Favorite.objects.filter(
            user=request.user, 
            game__in=latest_games
        ).values_list('game_id', flat=True)
    
    context = {
        'title': 'Главная страница',
        'latest_games': latest_games,
        'popular_collections': popular_collections,
        'favorite_game_ids': list(favorite_game_ids),  
    }
    return render(request, 'main/home.html', context)

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, game=game).exists()
    
    user_collections = []
    if request.user.is_authenticated:
        user_collections = Collection.objects.filter(user=request.user)
        
        for collection in user_collections:
            collection.game_is_added = collection.games.filter(id=game.id).exists()
    
    context = {
        'title': game.title,
        'game': game,
        'is_favorite': is_favorite,
        'user_collections': user_collections,
    }
    return render(request, 'main/game_detail.html', context)

def recommendations(request):
    all_tags = Tag.objects.all().order_by('name')
    
    context = {
        'title': 'Рекомендации',
        'all_tags': all_tags,
    }
    return render(request, 'main/recommendations.html', context)

def get_recommendations(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            include_tags_names = data.get('include_tags', [])
            exclude_tags_names = data.get('exclude_tags', [])
            
            include_tags = Tag.objects.filter(name__in=include_tags_names)
            exclude_tags = Tag.objects.filter(name__in=exclude_tags_names)
            
            games = Game.objects.all()
            
            if include_tags:
                for tag in include_tags:
                    games = games.filter(tags=tag)
            
            if exclude_tags:
                games = games.exclude(tags__in=exclude_tags)

            games = games.distinct()
            games = games.order_by('-rating')
            recommended_games = []
            for game in games:
                recommended_games.append({
                    'id': game.id,
                    'title': game.title,
                    'genres': game.get_genre_display(),
                    'release_year': game.release_year,
                    'rating': float(game.rating),
                    'price': int(game.price),
                    'game_image': game.game_image,
                    'developer': game.developer,
                    'tags': [tag.name for tag in game.tags.all()]
                })
            
            return JsonResponse({
                'success': True,
                'games': recommended_games,
                'count': len(recommended_games)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Только POST запросы'
    })

def search(request):
    query = request.GET.get('q', '').strip()
    games = []
    results_count = 0
    
    if query:
        games = list(Game.objects.filter(title__icontains=query).order_by('-rating')[:50])
        results_count = len(games)
    
    context = {
        'title': 'Поиск игр',
        'games': games,
        'query': query,
        'results_count': results_count
    }
    return render(request, 'main/search.html', context)

@login_required
def favorites(request):
    favorite_games = Game.objects.filter(
        favorite__user=request.user
    ).order_by('-favorite__added_at')
    
    favorite_collections = Collection.objects.filter(
        collectionlike__user=request.user
    ).exclude(user=request.user).order_by('-collectionlike__created_at')
    
    for collection in favorite_collections:
        collection.likes_count = collection.collectionlike_set.count()
    
    context = {
        'title': 'Избранное',
        'favorite_games': favorite_games,
        'favorite_collections': favorite_collections,
    }
    return render(request, 'main/favorites.html', context)

def collections(request):
    query = request.GET.get('q', '').strip()
    
    my_collections = None
    if request.user.is_authenticated:
        my_collections = Collection.objects.filter(user=request.user)
    
    popular_collections = Collection.objects.filter(
        is_public=True
    )
    
    if request.user.is_authenticated:
        popular_collections = popular_collections.exclude(user=request.user)
    
    popular_collections = popular_collections.annotate(
        like_count=Count('collectionlike')
    ).order_by('-like_count', '-created_at')
    
    if query:
        if my_collections is not None: 
            my_collections = my_collections.filter(title__icontains=query)
        popular_collections = popular_collections.filter(title__icontains=query)
    
    context = {
        'title': 'Подборки',
        'my_collections': my_collections, 
        'popular_collections': popular_collections,
        'query': query,
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'main/collections.html', context)

def collection_detail(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    
    is_owner = request.user.is_authenticated and collection.user == request.user
    
    is_favorite = False
    if request.user.is_authenticated and not is_owner:
        is_favorite = CollectionLike.objects.filter(
            user=request.user, 
            collection=collection
        ).exists()
    
    games_in_collection = Game.objects.filter(
        gamecollection__collection=collection
    ).order_by('gamecollection__order')
    
    collection.likes_count = collection.collectionlike_set.count()
    
    all_games = Game.objects.all()
    
    form = None
    if is_owner and request.method == 'POST':
        if 'edit_collection' in request.POST:
            form = CollectionForm(request.POST, instance=collection)
            if form.is_valid():
                form.save()
                messages.success(request, 'Подборка успешно обновлена!')
                return redirect('collection_detail', collection_id=collection.id)
        elif 'add_game' in request.POST:
            game_id = request.POST.get('game_id')
            if game_id:
                game = get_object_or_404(Game, id=game_id)
                if not GameCollection.objects.filter(collection=collection, game=game).exists():
                    from django.db.models import Max
                    max_order = GameCollection.objects.filter(
                        collection=collection
                    ).aggregate(Max('order'))['order__max'] or 0
                    
                    GameCollection.objects.create(
                        collection=collection,
                        game=game,
                        order=max_order + 1
                    )
                    messages.success(request, f'Игра "{game.title}" добавлена в подборку!')
                else:
                    messages.warning(request, 'Эта игра уже есть в подборке')
                return redirect('collection_detail', collection_id=collection.id)
    
    if not form and is_owner:
        form = CollectionForm(instance=collection)
    
    context = {
        'title': collection.title,
        'collection': collection,
        'games': games_in_collection,
        'all_games': all_games, 
        'is_owner': is_owner,
        'is_favorite': is_favorite,
        'form': form,
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'main/collection_detail.html', context)

@login_required
def add_game_to_collection(request, collection_id):
    """Добавить игру в подборку со страницы игры"""
    collection = get_object_or_404(Collection, id=collection_id)
    
    if collection.user != request.user:
        return JsonResponse({
            'status': 'error', 
            'message': 'Вы не можете добавлять игры в чужую подборку'
        }, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            game_id = data.get('game_id')
            
            if not game_id:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'ID игры не указан'
                }, status=400)
            
            game = get_object_or_404(Game, id=game_id)
            
            if GameCollection.objects.filter(collection=collection, game=game).exists():
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Эта игра уже есть в подборке'
                }, status=400)
            
            from django.db.models import Max
            max_order = GameCollection.objects.filter(
                collection=collection
            ).aggregate(Max('order'))['order__max'] or 0
            
            GameCollection.objects.create(
                collection=collection,
                game=game,
                order=max_order + 1
            )
            
            return JsonResponse({
                'status': 'success', 
                'message': f'Игра "{game.title}" добавлена в подборку "{collection.title}"'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error', 
                'message': 'Неверный формат данных'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': f'Ошибка: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'status': 'error', 
        'message': 'Неверный метод запроса'
    }, status=405)

@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {
        'title': 'Профиль',
        'user': request.user
    }
    return render(request, 'main/profile.html', context)

def about(request):
    context = {
        'title': 'О нас',
    }
    return render(request, 'main/about.html', context)

def contact(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Ваше сообщение успешно отправлено! Мы ответим вам в ближайшее время.')
            return redirect('contact') 
    else:
        form = FeedbackForm()
    
    context = {
        'title': 'Обратная связь',
        'form': form
    }
    return render(request, 'main/contact.html', context)

@login_required
def feedback_list(request):
    if not request.user.is_staff:
        return redirect('home')
    
    feedbacks = Feedback.objects.all()
    context = {
        'title': 'Сообщения обратной связи',
        'feedbacks': feedbacks
    }
    return render(request, 'main/feedback_list.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'main/register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
        
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            error = "Неверное имя пользователя или пароль"
    
    context = {
        'title': 'Вход в систему',
        'error': error
    }
    return render(request, 'main/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def toggle_favorite_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    if request.method == 'POST':
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            game=game
        )
        
        if not created:
            favorite.delete()
            return JsonResponse({'status': 'removed', 'message': 'Удалено из избранного'})
        else:
            return JsonResponse({'status': 'added', 'message': 'Добавлено в избранное'})
    
    return JsonResponse({'status': 'error', 'message': 'Неверный запрос'})

@login_required
def toggle_favorite_collection(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    
    if collection.user == request.user:
        return JsonResponse({
            'status': 'error', 
            'message': 'Нельзя добавить свою собственную подборку в избранное'
        })
    
    if request.method == 'POST':
        like, created = CollectionLike.objects.get_or_create(
            user=request.user,
            collection=collection
        )
        
        if not created:
            like.delete()
            likes_count = collection.collectionlike_set.count()
            return JsonResponse({
                'status': 'removed', 
                'message': 'Удалено из избранного',
                'likes_count': likes_count
            })
        else:
            likes_count = collection.collectionlike_set.count()
            return JsonResponse({
                'status': 'added', 
                'message': 'Добавлено в избранное',
                'likes_count': likes_count
            })
    
    return JsonResponse({'status': 'error', 'message': 'Неверный запрос'})

@login_required
def create_collection(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.user = request.user
            collection.save()
            messages.success(request, 'Подборка успешно создана!')
            return redirect('collection_detail', collection_id=collection.id)
    else:
        form = CollectionForm()
    
    context = {
        'title': 'Создать подборку',
        'form': form,
    }
    return render(request, 'main/create_collection.html', context)

@login_required
def remove_game_from_collection(request, collection_id, game_id):
    collection = get_object_or_404(Collection, id=collection_id)
    
    if collection.user != request.user:
        return redirect('collection_detail', collection_id=collection.id)
    
    game = get_object_or_404(Game, id=game_id)
    GameCollection.objects.filter(collection=collection, game=game).delete()
    
    messages.success(request, f'Игра "{game.title}" удалена из подборки')
    return redirect('collection_detail', collection_id=collection.id)

@login_required
def delete_collection(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    
    if collection.user != request.user:
        return redirect('collections')
    
    collection.delete()
    messages.success(request, 'Подборка успешно удалена!')
    return redirect('collections')