# ReelDeal

**Консольное Python-приложение для работы с учебной базой данных Sakila.**

---

## Описание
  
Приложение реализует:
- Поиск фильмов и актёров
- Фильтрацию по жанру, актёру, году выпуска
- Просмотр карточек фильмов и актёров
- Постраничный вывод (пагинация)
- Возврат (back), хлебные крошки, топы запросов
- Логирование команд и поисковых запросов

---

## Установка

1. **Клонируйте репозиторий:**
git clone https://github.com/Mihail0123/ReelDeal.git
cd ReelDeal

2. **Создайте и активируйте виртуальное окружение (рекомендуется):**
python -m venv .venv

Для Windows:
.venv\Scripts\activate

Для Linux/Mac:
source .venv/bin/activate


3. **Установите зависимости:**
pip install mysql-connector-python python-dotenv


4. **Создайте файл .env в корне проекта и пропишите параметры подключения к БД Sakila:**


---

## Запуск

python main.py



## Использование

- После запуска вы увидите приветствие и список команд.
- Вводите команды согласно подсказкам (например, `search Matrix`, `categories`, `actors`, `filter Action Pitt 2006`, `back`, `home`, `exit`).
- Для перехода по спискам используйте номера, для навигации — команды `next`, `prev`, `back`, `home`.

---

## Зависимости

- Python 3.8+
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## Структура проекта

ReelDeal/
├── main.py
├── config.py
├── db.py
├── models.py
├── repository.py
├── views.py
├── .env
├── .gitignore

