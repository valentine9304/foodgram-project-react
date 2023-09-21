`Python` `Django` `Django Rest Framework` `Docker` `Gunicorn` `NGINX`

`PostgreSQL` `Yandex Cloud` `Continuous Integration` `Continuous Deployment`

Проект развернут по адресу http://158.160.79.202

[Админ-зона проекта](http://158.160.79.202/admin/ "Гиперссылка к админке.")

Документация к [API](http://158.160.79.202/api/docs/ "Гиперссылка к API.") с актуальными адресами. Здесь описана структура возможных запросов и ожидаемых ответов.

## Проект Foodgram
Приложение «Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 

### Запуск проекта на удалённом сервере:
+ Клонировать репозиторий на локальный сервер:
```
git clone git@github.com:valentine9304/foodgram-project-react.git
```
+ Зайти на удалённый сервер:
```
ssh <Имя пользователя>@<IP адресс сервера>
```
+ Установить на сервере Docker, Docker Compose:
```
sudo apt install curl                                   - Установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      - Скачать скрипт для установки
sh get-docker.sh                                        - Запуск скрипта
sudo apt-get install docker-compose-plugin              - Последняя версия docker compose
```
+ Скопировать на сервер файлы docker-compose.yml, nginx.conf из папки infra (команды выполнять находясь в папке infra):
```
scp docker-compose.yml nginx.conf <Имя пользователя>@<IP адресс сервера>:/home/<Имя пользователя>/
```
+ В директории infra создать файл .env и заполнить своими данными:
```
SECRET_KEY= # Секретный ключ Django
DEBUG = False
DB_ENGINE=django.db.backends.postgresql # Указать базу PostgreSQL
DB_NAME=postgres #Имя базы
POSTGRES_USER=postgres #Логин
POSTGRES_PASSWORD=postgres #Пароль
DB_HOST=db #Название контейнера
DB_PORT=5432 # Порт для работы с БД
```

+ Создать и запустить контейнеры Docker, выполнить команду на сервере в папке с docker-compose.yml
  
Чтобы логи не мешали управлять контейнерами через терминал, развёртывание контейнеров выполняется в «фоновом режиме»: для этого применяется ключ -d
```
sudo docker-compose up -d --build
```
+ После закуска контейнеров выполните миграцию, создайте суперпользователя, соберите статику и загрузите данные из дампа в базу:
```
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
sudo docker-compose exec backend python manage.py loaddata dump.json
```
+ Для остановки контейнеров Docker:
```
sudo docker compose down -v      - с удалением контейнеров
sudo docker compose stop         - без удаления
```


## Авторы
:trollface: Валентин :sunglasses:  
