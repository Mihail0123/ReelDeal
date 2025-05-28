ReelDeal
Консольное Python-приложение для фильтраци и поиска фильмов/актёров из базы данных Sakila.

Описание
ReelDeal - это учебный проект для практики работы с базой данных на Python.

Приложение реализует:

Поиск фильмов и актёров

Фильтрацию по жанру, актёру, году выпуска

Просмотр карточек фильмов и актёров

Постраничный вывод (пагинация)

Возврат (back), хлебные крошки, топы запросов

Логирование команд и поисковых запросов

Установка
Клонируйте репозиторий:

git clone https://github.com/Mihail0123/ReelDeal.git
cd ReelDeal

Создайте и активируйте виртуальное окружение (рекомендуется):
python -m venv .venv
# Для Windows:
.venv\Scripts\activate
# Для Linux/Mac:
source .venv/bin/activate
Установите зависимости:


pip install mysql-connector-python python-dotenv
Создайте файл .env в корне проекта и пропишите параметры подключения к БД:


DB_HOST=ich-edit.edu.itcareerhub.de
DB_PORT=3306
DB_USER=ich1
DB_PASSWORD=ich1_password_ilovedbs
DB_NAME=sakila
Убедитесь, что у вас есть доступ к учебной базе Sakila.

Запуск
text
python main.py

Использование
После запуска вы увидите приветствие и список команд.

Вводите команды согласно подсказкам (например, search Matrix, categories, actors, filter Action Pitt 2006, back, home, exit).

Для перехода по спискам используйте номера, для навигации - команды next, prev, back, home.

Зависимости
Python 3.8+

mysql-connector-python

python-dotenv

Структура проекта
text
ReelDeal/
- main.py
- config.py
- db.py
- models.py
- repository.py
- views.py
- .env
- .gitignore
