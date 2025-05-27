# Содержит класс Repository, который реализует все методы работы с БД.
# Методы сгруппированы по сущностям (фильмы, актёры, категории, логирование).
# Использует курсор, полученный из db_session().

from models import Film, Actor, Category

class Repository:
    """
    Универсальный репозиторий для работы с БД.
    Все методы принимают self.cursor (курсор MySQL).
    Методы возвращают списки объектов моделей (Film, Actor, Category)
    или отдельные объекты (например, случайный фильм).
    """
    def __init__(self, cursor):
        self.cursor = cursor

    # --- Фильмы ---
    def get_films_by_category(self, category_id):
        """
        Возвращает список фильмов по id категории.
        """
        self.cursor.execute("""
            SELECT f.film_id, f.title, f.release_year, f.description, c.name
            FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
            WHERE c.category_id = %s
            ORDER BY f.title
        """, (category_id,))
        return [Film(*row) for row in self.cursor.fetchall()]

    def search_films(self, keyword):
        """
        Возвращает список фильмов, название которых содержит keyword.
        """
        self.cursor.execute("""
            SELECT f.film_id, f.title, f.release_year, f.description, c.name
            FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
            WHERE f.title LIKE %s
            ORDER BY f.title
        """, (f"%{keyword}%",))
        return [Film(*row) for row in self.cursor.fetchall()]

    def filter_films(self, genre=None, actor=None, year=None):
        """
        Фильтрация фильмов по жанру, актёру и/или году.
        Любой из параметров может быть None или '_', тогда фильтр не применяется.
        """
        query = """
            SELECT DISTINCT f.film_id, f.title, f.release_year, f.description, c.name
            FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
            JOIN film_actor fa ON f.film_id = fa.film_id
            JOIN actor a ON fa.actor_id = a.actor_id
            WHERE 1=1
        """
        params = []
        if genre and genre != '_':
            query += " AND c.name LIKE %s"
            params.append(f"%{genre}%")
        if actor and actor != '_':
            query += " AND CONCAT(a.first_name, ' ', a.last_name) LIKE %s"
            params.append(f"%{actor}%")
        if year and year != '_':
            query += " AND f.release_year = %s"
            params.append(year)
        query += " ORDER BY f.title"
        self.cursor.execute(query, tuple(params))
        return [Film(*row) for row in self.cursor.fetchall()]

    def get_random_film(self):
        """
        Возвращает случайный фильм из базы.
        """
        self.cursor.execute("""
            SELECT f.film_id, f.title, f.release_year, f.description, c.name
            FROM film f
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
            ORDER BY RAND()
            LIMIT 1
        """)
        row = self.cursor.fetchone()
        return Film(*row) if row else None

    # --- Актёры ---
    def get_top_actors(self, limit=10):
        """
        Возвращает топ-10 актёров по количеству фильмов.
        """
        self.cursor.execute("""
            SELECT a.first_name, a.last_name, COUNT(*) as film_count
            FROM actor a
            JOIN film_actor fa ON a.actor_id = fa.actor_id
            GROUP BY a.actor_id
            ORDER BY film_count DESC
            LIMIT %s
        """, (limit,))
        return [Actor(*row) for row in self.cursor.fetchall()]

    def get_all_actors(self):
        """
        Возвращает всех актёров по алфавиту.
        """
        self.cursor.execute("""
            SELECT first_name, last_name FROM actor ORDER BY last_name, first_name
        """)
        return [Actor(first, last) for first, last in self.cursor.fetchall()]

    def get_actors_by_film_id(self, film_id):
        """
        Возвращает список актёров для заданного фильма.
        """
        self.cursor.execute("""
            SELECT a.first_name, a.last_name
            FROM actor a
            JOIN film_actor fa ON a.actor_id = fa.actor_id
            WHERE fa.film_id = %s
            ORDER BY a.last_name, a.first_name
        """, (film_id,))
        return [Actor(first, last) for first, last in self.cursor.fetchall()]

    def get_films_by_actor(self, actor_name):
        """
        Возвращает список фильмов, в которых снимался актёр (по имени).
        """
        self.cursor.execute("""
            SELECT f.film_id, f.title, f.release_year, f.description, c.name
            FROM film f
            JOIN film_actor fa ON f.film_id = fa.film_id
            JOIN actor a ON fa.actor_id = a.actor_id
            JOIN film_category fc ON f.film_id = fc.film_id
            JOIN category c ON fc.category_id = c.category_id
            WHERE CONCAT(a.first_name, ' ', a.last_name) LIKE %s
            ORDER BY f.title
        """, (f"%{actor_name}%",))
        return [Film(*row) for row in self.cursor.fetchall()]

    # --- Категории ---
    def get_categories(self):
        """
        Возвращает список всех категорий (жанров).
        """
        self.cursor.execute("SELECT category_id, name FROM category ORDER BY name")
        return [Category(cat_id, name) for cat_id, name in self.cursor.fetchall()]

    # --- Логирование и топы ---
    def create_search_log_table(self):
        """
        Создаёт таблицу логов поисковых запросов, если не существует.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_search_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                search_query VARCHAR(255) NOT NULL,
                search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def create_command_log_table(self):
        """
        Создаёт таблицу логов всех команд, если не существует.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS all_command_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                command_text VARCHAR(255),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def log_search(self, query):
        """
        Записывает поисковый запрос в лог.
        """
        self.cursor.execute("INSERT INTO student_search_log (search_query) VALUES (%s)", (query,))

    def log_command(self, command):
        """
        Записывает команду пользователя в лог.
        """
        self.cursor.execute("INSERT INTO all_command_log (command_text) VALUES (%s)", (command,))

    def get_top_queries(self, limit=10):
        """
        Возвращает топ поисковых запросов.
        """
        self.cursor.execute("""
            SELECT search_query
            FROM student_search_log
            GROUP BY search_query
            ORDER BY COUNT(*) DESC
            LIMIT %s
        """, (limit,))
        return [row[0] for row in self.cursor.fetchall()]

    def get_top_commands(self, limit=15):
        """
        Возвращает топ команд пользователя.
        """
        self.cursor.execute("""
            SELECT command_text, COUNT(*) as count
            FROM all_command_log
            GROUP BY command_text
            ORDER BY count DESC
            LIMIT %s
        """, (limit,))
        return list(self.cursor.fetchall())
