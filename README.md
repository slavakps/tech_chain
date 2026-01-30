# Tech Chain API

## Описание:

Tech Chain — это веб-приложение на Django и Django REST Framework, реализующее иерархическую сеть по продаже электроники (завод → розничная сеть → индивидуальный предприниматель).  
Приложение предоставляет REST API и административную панель для управления звеньями сети и продуктами.

---

## Стек технологий

- Python  
- Django  
- Django REST Framework  
- PostgreSQL  
- Poetry  

---

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/slavakps/tech-chain.git
cd tech-chain
```

2. Установите зависимости:
```
poetry install
```

3. Создайте файл переменных окружения:
```
cp .env.example .env
```

4. Заполните файл `.env`:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=tech_chain_db
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

5. Примените миграции:
```
python manage.py migrate
```

6. Создайте суперпользователя:
```
python manage.py createsuperuser
```

7. Запустите сервер:
```
python manage.py runserver
```

---

## Использование

**Админ-панель:**  
http://127.0.0.1:8000/admin/

**API узлов сети:**  
http://127.0.0.1:8000/api/network-nodes/

**Получение токена:**  
```
POST http://127.0.0.1:8000/api/token/
```

---

## Возможности API

- CRUD операции для звеньев сети  
- Вложенные продукты в ответах  
- Фильтрация по стране  
- Запрет изменения задолженности через API  
- Доступ только для активных пользователей  


---

## Переменные окружения

Файл `.env` обязателен и не должен попадать в репозиторий.

---

## Требования

- Python 3.12+  
- PostgreSQL 10+  

---

## Лицензия

Проект выполнен в рамках тестового задания.
