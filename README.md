# RecGames — платформа рекомендаций видеоигр

RecGames — это веб-приложение на Django для подбора и хранения видеоигр.
Пользователь может просматривать игры, рекомендовать их по тегам,
добавлять игры в коллекции и оставлять обратную связь.

Проект реализован в учебных целях и демонстрирует работу с Django ORM,
аутентификацией пользователей, формами, шаблонами и базой данных.

## Features

- Регистрация и авторизация пользователей
- Рекомендация игр по тегам
- Коллекции игр пользователя
- Поиск игр
- Форма обратной связи
- Административная панель Django

## Tech Stack

**Backend:**

- Python
- Django
- Django ORM

**Database:**

- SQLite

**Frontend:**

- HTML
- CSS
- Django Templates

**Libraries:**

- django
- pillow

## Installation

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/RecGames.git
cd RecGames
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
```

### 3. Активация виртуального окружения

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 5. Применение миграций

```bash
python manage.py migrate
```

### 6. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запуск сервера

```bash
python manage.py runserver
```

Приложение доступно по адресу:  
http://127.0.0.1:8000/

## Screenshots

### Главная страница

<img width="1858" height="1053" alt="изображение" src="https://github.com/user-attachments/assets/fd47c57c-ce5b-4964-9690-a6d26454a18a" />

### Страница игры

<img width="1858" height="1053" alt="image" src="https://github.com/user-attachments/assets/55e31a83-1dd8-471a-94be-1d78d76f640a" />

### Страница рекомендаций

<img width="1858" height="1053" alt="image" src="https://github.com/user-attachments/assets/b66d5e77-7ab6-4a9e-b5f3-82bc664b0ffc" />

### Страница подборок

<img width="1858" height="1053" alt="image" src="https://github.com/user-attachments/assets/45c1754c-3223-4864-baa1-018057e43b1a" />

### Страница избранного

<img width="1858" height="1053" alt="image" src="https://github.com/user-attachments/assets/d9f98fe4-dc12-4b5a-a3d1-87307e289855" />

## ER-диаграмма

<img width="1180" height="708" alt="image" src="https://github.com/user-attachments/assets/1ff16b53-d0a6-4e85-9a02-f7f87d2b3a77" />

## Архитектурная схема

<img width="1357" height="724" alt="image" src="https://github.com/user-attachments/assets/8737a1c1-e99f-465e-818f-a301f05440d1" />
