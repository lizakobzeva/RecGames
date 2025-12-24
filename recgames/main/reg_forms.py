from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Введите email', 'style': 'width: 100%; padding: 8px;'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Введите имя пользователя',
            'style': 'width: 100%; padding: 8px;'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Введите пароль',
            'style': 'width: 100%; padding: 8px;'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Повторите пароль',
            'style': 'width: 100%; padding: 8px;'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email