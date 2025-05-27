# models.py
# Содержит простые классы-модели для бизнес-объектов:
# Film, Actor, Category. Используются для удобства работы с данными,
# полученными из БД (вместо кортежей).

class Film:
    """
    Модель фильма.
    Аргументы конструктора:
        film_id: int — идентификатор фильма
        title: str — название фильма
        year: int — год выпуска
        description: str — описание
        genre: str — жанр
    """
    def __init__(self, film_id, title, year, description, genre):
        self.film_id = film_id
        self.title = title
        self.year = year
        self.description = description
        self.genre = genre

    def get_short_description(self, max_length=60):
        """
        Возвращает сокращённое описание фильма.
        Если описание длиннее max_length, обрезает и добавляет "...".
        """
        return self.description if len(self.description) <= max_length else self.description[:max_length] + "..."

class Actor:
    """
    Модель актёра.
    Аргументы конструктора:
        first_name: str — имя
        last_name: str — фамилия
        film_count: int (опционально) — количество фильмов (для топа)
    """
    def __init__(self, first_name, last_name, film_count=None):
        self.first_name = first_name
        self.last_name = last_name
        self.film_count = film_count

    def full_name(self):
        """
        Возвращает полное имя актёра.
        """
        return f"{self.first_name} {self.last_name}"

class Category:
    """
    Модель категории (жанра).
    Аргументы конструктора:
        category_id: int — идентификатор категории
        name: str — название жанра
    """
    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name
