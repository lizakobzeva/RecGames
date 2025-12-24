# RecGames — платформа рекомендаций видеоигр

RecGames — это веб-приложение на Django для подбора и хранения видеоигр.
Пользователь может просматривать игры, фильтровать их по жанрам и тегам,
добавлять игры в коллекции и оставлять обратную связь.

Проект реализован в учебных целях и демонстрирует работу с Django ORM,
аутентификацией пользователей, формами, шаблонами и базой данных.

## Features

- Регистрация и авторизация пользователей
- Каталог видеоигр
- Фильтрация игр по жанрам и тегам
- Коллекции игр пользователя
- Система тегов
- Форма обратной связи
- Административная панель Django

## Tech Stack

**Backend:**

- Python 3.10
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

![](docs/screenshots/main_page.png)

### Каталог игр

![](docs/screenshots/games_list.png)

### Страница игры

![](docs/screenshots/game_detail.png)

### Форма обратной связи

![](docs/screenshots/feedback.png)

## Database ER Diagram

![](docs/er_diagram.png)

## API

В проекте отсутствует REST API.  
Взаимодействие осуществляется через Django views и HTML-шаблоны.

## Architecture

![](docs/architecture.png)

## Code Documentation

В ключевых моделях, представлениях и формах используются docstrings
для пояснения логики работы кода.
