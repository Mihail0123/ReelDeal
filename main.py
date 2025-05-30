# Обработка команд пользователя, навигация, стек возврата, хлебные крошки, пагинация.
# Вся работа с БД — через Repository, все выводы — через views.py.

from db import db_session
from repository import Repository
from views import (
    show_welcome, show_help, show_error, show_breadcrumb, show_categories,
    show_top_actors, show_actors_list, show_search_results, show_film_details,
    show_top_queries, show_exit_message
)
from models import Film, Actor, Category

PAGE_SIZE = 15  # Количество элементов на странице для пагинации

def paginate(items, page, page_size=PAGE_SIZE):
    """
    Вспомогательная функция для постраничного вывода.
    Возвращает срез списка для текущей страницы и строку с инфо о странице.
    """
    total = len(items)
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    start = (page - 1) * page_size
    end = min(start + page_size, total)
    page_items = items[start:end]
    page_info = f"Страница {page}/{total_pages} (элементы {start+1}-{end} из {total})"
    return page_items, page_info, total_pages

def main():
    # Основные переменные состояния
    context_stack = []  # Стек для возврата (back)
    current_context = 'home'
    breadcrumb = 'Главная'
    paginator = {'page': 1, 'total_pages': 1}
    current_data = []  # Текущий список элементов (фильмы, актёры и т.д.)
    current_section = ''  # Для заголовков (например, "поиск", "фильтр")

    with db_session() as cursor:
        repo = Repository(cursor)
        # Создаём таблицы логов, если их нет
        repo.create_search_log_table()
        repo.create_command_log_table()

        show_welcome()
        show_help()

        while True:
            cmd = input("\n> ").strip()
            if not cmd:
                continue
            repo.log_command(cmd)


            # Пагинация
            if cmd == 'next':
                if paginator['page'] < paginator['total_pages']:
                    paginator['page'] += 1
                    refresh_display(current_context, current_data, paginator, breadcrumb, current_section)
                else:
                    show_error("Вы уже на последней странице")
                continue
            if cmd == 'prev':
                if paginator['page'] > 1:
                    paginator['page'] -= 1
                    refresh_display(current_context, current_data, paginator, breadcrumb, current_section)
                else:
                    show_error("Вы уже на первой странице")
                continue

            # Возврат (back)
            if cmd == 'back':
                if context_stack:
                    state = context_stack.pop()
                    current_context = state['context']
                    breadcrumb = state['breadcrumb']
                    current_data = state['data']
                    paginator = state['paginator']
                    current_section = state.get('section', '')
                    show_breadcrumb(breadcrumb)
                    refresh_display(current_context, current_data, paginator, breadcrumb, current_section)
                    if current_context == 'home':
                        show_welcome()
                        show_help()
                else:
                    show_error("Нет предыдущего экрана.")
                continue

            # Главная (home)
            if cmd == 'home':
                current_context = 'home'
                breadcrumb = 'Главная'
                context_stack.clear()
                paginator = {'page': 1, 'total_pages': 1}
                current_data = []
                current_section = ''
                show_welcome()
                show_help()
                continue

            # Выход
            if cmd == 'exit':
                show_exit_message()
                break

            # Справка
            if cmd == 'help':
                show_help()
                continue

            # --- Основные команды ---
            if cmd == 'categories':
                categories = repo.get_categories()
                context_stack.append({
                    'context': current_context,
                    'breadcrumb': breadcrumb,
                    'data': current_data,
                    'paginator': paginator.copy(),
                    'section': current_section
                })
                current_context = 'categories'
                breadcrumb = 'Главная > Категории'
                current_data = categories
                paginator = {'page': 1, 'total_pages': 1}
                show_breadcrumb(breadcrumb)
                show_categories(categories)
                continue

            if cmd == 'actors':
                top_actors = repo.get_top_actors()
                all_actors = repo.get_all_actors()
                context_stack.append({
                    'context': current_context,
                    'breadcrumb': breadcrumb,
                    'data': current_data,
                    'paginator': paginator.copy(),
                    'section': current_section
                })
                current_context = 'actors'
                breadcrumb = 'Главная > Актёры'
                current_data = all_actors
                paginator['page'] = 1
                page_items, page_info, total_pages = paginate(all_actors, paginator['page'])
                paginator['total_pages'] = total_pages
                show_breadcrumb(breadcrumb)
                show_top_actors(top_actors)
                show_actors_list(page_items, page_info)
                continue

            if cmd == 'top_queries':
                queries = repo.get_top_commands()
                context_stack.append({
                    'context': current_context,
                    'breadcrumb': breadcrumb,
                    'data': current_data,
                    'paginator': paginator.copy(),
                    'section': current_section
                })
                current_context = 'top_queries'
                breadcrumb = 'Главная > Популярные команды'
                current_data = queries
                paginator['page'] = 1
                page_items, page_info, total_pages = paginate(queries, paginator['page'])
                paginator['total_pages'] = total_pages
                show_breadcrumb(breadcrumb)
                show_top_queries(page_items, page_info)
                continue

            if cmd == 'random':
                film = repo.get_random_film()
                if film:
                    actors = repo.get_actors_by_film_id(film.film_id)
                    context_stack.append({
                        'context': current_context,
                        'breadcrumb': breadcrumb,
                        'data': current_data,
                        'paginator': paginator.copy(),
                        'section': current_section
                    })
                    current_context = 'film'
                    breadcrumb = f"Главная > Случайный фильм > {film.title}"
                    current_data = [film]
                    paginator = {'page': 1, 'total_pages': 1}
                    show_breadcrumb(breadcrumb)
                    show_film_details(film, actors)
                else:
                    show_error("Не удалось получить случайный фильм.")
                continue

            # --- Поиск и фильтрация ---
            if cmd.startswith("search "):
                keyword = cmd[7:].strip()
                results = repo.search_films(keyword)
                repo.log_search(keyword)
                context_stack.append({
                    'context': current_context,
                    'breadcrumb': breadcrumb,
                    'data': current_data,
                    'paginator': paginator.copy(),
                    'section': current_section
                })
                current_context = 'search'
                breadcrumb = f"Главная > Поиск: {keyword}"
                current_data = results
                paginator['page'] = 1
                page_items, page_info, total_pages = paginate(results, paginator['page'])
                paginator['total_pages'] = total_pages
                current_section = "поиск"
                show_breadcrumb(breadcrumb)
                show_search_results(page_items, page_info, section=current_section)
                continue

            if cmd.startswith("filter"):
                parts = cmd.split()
                genre = parts[1] if len(parts) > 1 else None
                actor = parts[2] if len(parts) > 2 else None
                year = parts[3] if len(parts) > 3 else None
                results = repo.filter_films(genre, actor, year)
                context_stack.append({
                    'context': current_context,
                    'breadcrumb': breadcrumb,
                    'data': current_data,
                    'paginator': paginator.copy(),
                    'section': current_section
                })
                current_context = 'filter'
                breadcrumb = "Главная > Фильтр"
                current_data = results
                paginator['page'] = 1
                page_items, page_info, total_pages = paginate(results, paginator['page'])
                paginator['total_pages'] = total_pages
                current_section = "фильтр"
                show_breadcrumb(breadcrumb)
                show_search_results(page_items, page_info, section=current_section)
                continue

            # --- Выбор по номеру ---
            if cmd.isdigit():
                idx = int(cmd)
                # Категории (без пагинации)
                if current_context == 'categories':
                    categories = current_data
                    if 1 <= idx <= len(categories):
                        category = categories[idx - 1]
                        films = repo.get_films_by_category(category.category_id)
                        context_stack.append({
                            'context': current_context,
                            'breadcrumb': breadcrumb,
                            'data': current_data,
                            'paginator': paginator.copy(),
                            'section': current_section
                        })
                        current_context = 'search'
                        breadcrumb = f"Главная > Категории > {category.name}"
                        current_data = films
                        paginator['page'] = 1
                        page_items, page_info, total_pages = paginate(films, paginator['page'])
                        paginator['total_pages'] = total_pages
                        current_section = "категория"
                        show_breadcrumb(breadcrumb)
                        show_search_results(page_items, page_info, section=current_section)
                    else:
                        show_error("Категория с таким номером не найдена.")
                    continue

                # Актёры (с пагинацией)
                if current_context == 'actors':
                    all_actors = current_data
                    page_items, page_info, total_pages = paginate(all_actors, paginator['page'])
                    if 1 <= idx <= len(page_items):
                        actor = page_items[idx - 1]
                        films = repo.get_films_by_actor(actor.full_name())
                        context_stack.append({
                            'context': current_context,
                            'breadcrumb': breadcrumb,
                            'data': current_data,
                            'paginator': paginator.copy(),
                            'section': current_section
                        })
                        current_context = 'search'
                        breadcrumb = f"Главная > Актёры > {actor.full_name()}"
                        current_data = films
                        paginator['page'] = 1
                        page_items, page_info, total_pages = paginate(films, paginator['page'])
                        paginator['total_pages'] = total_pages
                        current_section = "поиск по актёру"
                        show_breadcrumb(breadcrumb)
                        show_search_results(page_items, page_info, section=current_section)
                    else:
                        show_error("Неверный номер актёра.")
                    continue

                # Фильмы (поиск, фильтр, поиск по актёру)
                if current_context in ['search', 'filter', 'top_queries', 'actors']:
                    films = current_data
                    page_items, page_info, total_pages = paginate(films, paginator['page'])
                    if 1 <= idx <= len(page_items):
                        film = page_items[idx - 1]
                        actors = repo.get_actors_by_film_id(film.film_id)
                        context_stack.append({
                            'context': current_context,
                            'breadcrumb': breadcrumb,
                            'data': current_data,
                            'paginator': paginator.copy(),
                            'section': current_section
                        })
                        current_context = 'film'
                        breadcrumb = f"{breadcrumb} > {film.title}"
                        current_data = [film]
                        paginator = {'page': 1, 'total_pages': 1}
                        show_breadcrumb(breadcrumb)
                        show_film_details(film, actors)
                    else:
                        show_error("Неверный номер фильма.")
                    continue

                # Карточка фильма (выбор актёра)
                if current_context == 'film':
                    film = current_data[0]
                    actors = repo.get_actors_by_film_id(film.film_id)
                    if 1 <= idx <= len(actors):
                        actor = actors[idx - 1]
                        films = repo.get_films_by_actor(actor.full_name())
                        context_stack.append({
                            'context': current_context,
                            'breadcrumb': breadcrumb,
                            'data': current_data,
                            'paginator': paginator.copy(),
                            'section': current_section
                        })
                        current_context = 'search'
                        breadcrumb = f"{breadcrumb} > {actor.full_name()}"
                        current_data = films
                        paginator['page'] = 1
                        page_items, page_info, total_pages = paginate(films, paginator['page'])
                        paginator['total_pages'] = total_pages
                        current_section = "поиск по актёру"
                        show_breadcrumb(breadcrumb)
                        show_search_results(page_items, page_info, section=current_section)
                    else:
                        show_error("Неверный номер актёра.")
                    continue

            # --- Поиск по имени категории ---
            if current_context == 'categories':
                categories = current_data
                found = False
                for category in categories:
                    if cmd.lower() == category.name.lower():
                        films = repo.get_films_by_category(category.category_id)
                        context_stack.append({
                            'context': current_context,
                            'breadcrumb': breadcrumb,
                            'data': current_data,
                            'paginator': paginator.copy(),
                            'section': current_section
                        })
                        current_context = 'search'
                        breadcrumb = f"Главная > Категории > {category.name}"
                        current_data = films
                        paginator['page'] = 1
                        page_items, page_info, total_pages = paginate(films, paginator['page'])
                        paginator['total_pages'] = total_pages
                        current_section = "категория"
                        show_breadcrumb(breadcrumb)
                        show_search_results(page_items, page_info, section=current_section)
                        found = True
                        break
                if not found:
                    show_error("Категория не найдена.")
                continue

            # --- Поиск по имени актёра или названию фильма ---
            films = repo.search_films(cmd)
            if films:
                repo.log_search(cmd)
                context_stack.append({
                    'context': current_context,
                    'breadcrumb': breadcrumb,
                    'data': current_data,
                    'paginator': paginator.copy(),
                    'section': current_section
                })
                current_context = 'search'
                breadcrumb = f"Главная > Поиск: {cmd}"
                current_data = films
                paginator['page'] = 1
                page_items, page_info, total_pages = paginate(films, paginator['page'])
                paginator['total_pages'] = total_pages
                current_section = "поиск"
                show_breadcrumb(breadcrumb)
                show_search_results(page_items, page_info, section=current_section)
                continue
            films = repo.get_films_by_actor(cmd)
            if films:
                context_stack.append({
                    'context': current_context,
                    'breadcrumb': breadcrumb,
                    'data': current_data,
                    'paginator': paginator.copy(),
                    'section': current_section
                })
                current_context = 'search'
                breadcrumb = f"Главная > Актёры > {cmd}"
                current_data = films
                paginator['page'] = 1
                page_items, page_info, total_pages = paginate(films, paginator['page'])
                paginator['total_pages'] = total_pages
                current_section = "поиск по актёру"
                show_breadcrumb(breadcrumb)
                show_search_results(page_items, page_info, section=current_section)
                continue

            show_error("Неизвестная команда. Введите 'help' для списка команд.")

def refresh_display(current_context, current_data, paginator, breadcrumb, current_section):
    """
    Обновляет вывод текущего экрана (например, после next/prev/back).
    """
    show_breadcrumb(breadcrumb)
    if current_context == 'categories':
        show_categories(current_data)
    elif current_context == 'actors':
        page_items, page_info, _ = paginate(current_data, paginator['page'])
        show_actors_list(page_items, page_info)
    elif current_context in ['search', 'filter']:
        page_items, page_info, _ = paginate(current_data, paginator['page'])
        show_search_results(page_items, page_info, section=current_section)
    elif current_context == 'top_queries':
        page_items, page_info, _ = paginate(current_data, paginator['page'])
        show_top_queries(page_items, page_info)
    elif current_context == 'film':
        film = current_data[0]
        # Для карточки фильма всегда показываем всех актёров
        from repository import Repository  # Импорт тут, чтобы не было циклических
        with db_session() as cursor:
            repo = Repository(cursor)
            actors = repo.get_actors_by_film_id(film.film_id)
        show_film_details(film, actors)

if __name__ == "__main__":
    main()
