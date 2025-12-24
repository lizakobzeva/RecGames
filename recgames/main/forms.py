from django import forms
from .models import Feedback, Collection, Game

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваше сообщение', 'rows': 4}),
        }

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'description', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название подборки'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание подборки', 'rows': 3}),
        }

class AddGameToCollectionForm(forms.Form):
    game = forms.ModelChoiceField(
        queryset=Game.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Выберите игру'
    )