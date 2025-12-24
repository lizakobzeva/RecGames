from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'), 
    path('recommendations/', views.recommendations, name='recommendations'),
    path('recommendations/get/', views.get_recommendations, name='get_recommendations'), 
    path('search/', views.search, name='search'),
    path('favorites/', views.favorites, name='favorites'),
    path('collections/', views.collections, name='collections'),
    path('collection/<int:collection_id>/', views.collection_detail, name='collection_detail'),
    path('collection/create/', views.create_collection, name='create_collection'),
    path('collection/<int:collection_id>/delete/', views.delete_collection, name='delete_collection'),
    path('collection/<int:collection_id>/remove-game/<int:game_id>/', views.remove_game_from_collection, name='remove_game_from_collection'),
    path('game/<int:game_id>/toggle-favorite/', views.toggle_favorite_game, name='toggle_favorite_game'),
    path('collection/<int:collection_id>/toggle-favorite/', views.toggle_favorite_collection, name='toggle_favorite_collection'),
    path('collection/<int:collection_id>/add-game-ajax/', views.add_game_to_collection, name='add_game_to_collection_ajax'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]