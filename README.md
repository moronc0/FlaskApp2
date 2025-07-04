# Галерея изображений

Веб-приложение для обмена и управления изображениями, разработанное на Flask.

## Описание

Это веб-приложение представляет собой платформу для обмена изображениями с возможностью:
- Регистрации и авторизации пользователей
- Загрузки и управления изображениями
- Просмотра галереи изображений
- Фильтрации изображений по автору и тегам
- Редактирования профиля пользователя
- Административной панели

> **Важно**: Первый зарегистрированный пользователь автоматически получает права администратора. Убедитесь, что администратор регистрируется первым в системе.

## Технологии

- Python 3.x
- Flask 3.1.1
- SQLAlchemy 2.0.41
- Flask-Login
- Flask-RESTful
- Flask-WTF
- SQLite (база данных)

## Установка

1. Клонируйте репозиторий:
```bash
git clone [url-репозитория]
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
.venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите приложение:
```bash
python main.py
```

## Структура проекта

- `main.py` - основной файл приложения
- `blueprint_api/` - API endpoints
- `forms/` - формы для работы с данными
- `templates/` - HTML шаблоны
- `static/` - статические файлы
- `data/` - модели данных и работа с базой данных
- `tests/` - тесты
- `parsers/` - парсеры данных
- `resources/` - ресурсы API

## Функциональность

### Пользователи
- Регистрация с загрузкой фото профиля
- Авторизация
- Просмотр и редактирование профиля
- Управление своими изображениями

### Изображения
- Загрузка изображений
- Добавление описания и тегов
- Редактирование и удаление
- Просмотр галереи
- Фильтрация по автору и тегам

### Административная панель
- Управление пользователями
- Модерация контента

## API

Приложение предоставляет REST API для работы с:
- Пользователями
- Изображениями
 