# Инструкция по запуску проекта

## 1. Создание и активация виртуального окружения

```bash
python -m venv my_env
source venv/bin/activate
```

## 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 3. Запуск PostgreSQL через Docker

```bash
docker run --name hw-06 -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres
```

## 4. Создание миграции Alembic

```bash
alembic revision --autogenerate -m "Initial migration"
```

## 5. Заполнение базы данными

```bash
python seed.py
```

## 6. Выполнение запросов

```bash
python ./my_select.py
```

---

## 7. Додаткове завдання (CLI CRUD доступ до бази)

```bash
# Створити викладача
python main.py -a create -m Teacher -n "Boris Jonson"

# Показати всі групи
python main.py -a list -m Group

# Оновити викладача з id=3
python main.py -a update -m Teacher --id 3 -n "Andry Bezos"

# Видалити групу
python main.py -a remove -m Group --id 2
```