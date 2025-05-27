# Содержит функции для вывода информации пользователю.
# Все функции максимально просты, принимают только те данные, которые нужны для вывода.
# Не содержат бизнес-логики — только форматирование и печать.

def show_welcome():
    """
    Выводит ASCII-логотип и приветствие.
    """
    logo = r"""
8 888888888o.   8 8888888888   8 8888888888   8 8888         8 888888888o.      8 8888888888            .8.          8 8888
8 8888    `88.  8 8888         8 8888         8 8888         8 8888    `^888.   8 8888                 .888.         8 8888
8 8888     `88  8 8888         8 8888         8 8888         8 8888        `88. 8 8888                :88888.        8 8888
8 8888     ,88  8 8888         8 8888         8 8888         8 8888         `88 8 8888               . `88888.       8 8888
8 8888.   ,88'  8 888888888888 8 888888888888 8 8888         8 8888          88 8 888888888888      .8. `88888.      8 8888
8 888888888P'   8 8888         8 8888         8 8888         8 8888          88 8 8888             .8`8. `88888.     8 8888
8 8888`8b       8 8888         8 8888         8 8888         8 8888         ,88 8 8888            .8' `8. `88888.    8 8888
8 8888 `8b.     8 8888         8 8888         8 8888         8 8888        ,88' 8 8888           .8'   `8. `88888.   8 8888
8 8888   `8b.   8 8888         8 8888         8 8888         8 8888    ,o88P'   8 8888          .888888888. `88888.  8 8888
8 8888     `88. 8 888888888888 8 888888888888 8 888888888888 8 888888888P'      8 888888888888 .8'       `8. `88888. 8 888888888888
    """
    print(logo)
    print("Добро пожаловать в Reel Deal!")

def show_help():
    """
    Показывает справку по доступным командам.
    """
    print("""
    Доступные команды:
    help — Список команд
    categories — Список жанров
    actors — Топ актёров
    search <слово> — Поиск фильмов
    filter <жанр> <актёр> <год> — Фильтрация
    top_queries — Популярные запросы
    random — Случайный фильм
    next — Следующая страница
    prev — Предыдущая страница
    back — Назад
    home — Главная
    exit — Выход
    """)

def show_error(message):
    """
    Выводит сообщение об ошибке.
    """
    print(f"🚨 {message}")

def show_breadcrumb(breadcrumb):
    """
    Показывает навигационную цепочку (хлебные крошки).
    """
    print(f"[Путь: {breadcrumb}]")

def show_categories(categories):
    """
    Показывает список жанров (категорий).
    Аргументы:
        categories: список объектов Category
    """
    print("\nЖанры фильмов:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category.name}")
    print("\nВведите номер жанра или его название, или команду (back | home | help | exit)")

def show_top_actors(actors):
    """
    Показывает топ-10 актёров по количеству фильмов.
    Аргументы:
        actors: список объектов Actor (с film_count)
    """
    print("\nТоп-10 актёров по количеству фильмов:")
    for i, actor in enumerate(actors, start=1):
        print(f"{i}. {actor.full_name()} — {actor.film_count} фильмов")

def show_actors_list(actors, page_info=None):
    """
    Показывает список актёров (например, для пагинации).
    Аргументы:
        actors: список объектов Actor
        page_info: строка с информацией о странице (например, "Страница 1/3")
    """
    print("\nПолный список актёров по алфавиту:")
    for idx, actor in enumerate(actors, start=1):
        print(f"{idx}. {actor.full_name()}")
    if page_info:
        print(page_info)
    print("\nВведите номер актёра, next, prev или команду (back | home | help | exit)")

def show_search_results(films, page_info=None, section="поиск"):
    """
    Показывает результаты поиска или фильтрации фильмов.
    Аргументы:
        films: список объектов Film
        page_info: строка с информацией о странице (например, "Страница 2/5")
        section: строка для заголовка (например, "поиск", "фильтр")
    """
    if not films:
        print("Ничего не найдено.")
        return
    print(f"\nРезультаты (раздел: {section}):")
    for i, film in enumerate(films, start=1):
        print(f"{i}. {film.title} ({film.year}, жанр: {film.genre}) — {film.get_short_description()}")
    if page_info:
        print(page_info)
    print("\nВведите номер фильма, next, prev или команду (back | home | help | exit)")

def show_film_details(film, actors):
    """
    Показывает подробную информацию о фильме и его актёрах.
    Аргументы:
        film: объект Film
        actors: список объектов Actor
    """
    print(f"\nФильм: {film.title} ({film.year}, жанр: {film.genre})")
    print(f"Описание: {film.description}")
    print("\nАктёры:")
    for idx, actor in enumerate(actors, start=1):
        print(f"{idx}. {actor.full_name()}")
    print("\nВведите номер актёра, имя, или команду (back | home | help | exit)")

def show_top_queries(queries, page_info=None):
    """
    Показывает самые популярные команды или поисковые запросы.
    Аргументы:
        queries: список кортежей (command, count)
        page_info: строка с информацией о странице
    """
    print("\nСамые популярные команды:")
    for i, (command, count) in enumerate(queries, start=1):
        print(f"{i}. {command} — {count} раз")
    if page_info:
        print(page_info)
    print("\nВведите номер, next, prev или команду (back | home | help | exit)")

def show_exit_message():
    """
    Показывает финальное сообщение при выходе.
    """
    print("\nСпасибо за использование Reel Deal! До новых встреч! 🎬")
