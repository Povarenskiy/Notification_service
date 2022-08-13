# Сервис уведомлений

Сервис разработан на Django REST framefork


## Установка и запуск

1. Склонировать репозиторий с Github.com:
````
https://github.com/Povarenskiy/notification_service.git
````

2. В директории проекта создать виртуальное окружение (venv/ — название виртуального окружения)
````
python -m venv venv
````

3. Активировать виртуальное окружение 
````
venv\Scripts\activate.bat - для Windows
source venv/bin/activate - для Linux и MacOS
````

4. В файле settings.py указать личный токен: ```` TOKEN = '<личный токен>' ````
5. Установка зависимостей
````
pip install -r requirements.txt
````

6. Создать и применить миграции в базу данных
````
python manage.py makemigrations
python manage.py migrate
````

7. Запустить сервер
````
python manage.py runserver
````

## Api

````http://127.0.0.1:8000/api/```` - api проекта

````http://127.0.0.1:8000/api/client/```` - клиенты

````http://127.0.0.1:8000/api/mailing/```` - рассылки 

````http://127.0.0.1:8000/api/mailing/<pk>/callinfo/```` - детальная статистика по конкретной рассылке  

````http://127.0.0.1:8000/api/mailing/callfullinfo/```` - общая статистика по созданным рассылкам с группировкой по статусам

````http://127.0.0.1:8000/api/message/```` - сообщения 
