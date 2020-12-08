# REST API для YaMDb

YaMDb - база отзывов для фильмов, книг и музыки. В этом проекте мы реализовали REST API для сервиса YaMDb.   

## Начало работы

Запустить проект можно в контейнерах Docker. Для этого подготовлены конфигурационные файлы Dockerfile и docker-compose.yaml.  

### Подготовка к запуску

Для запуска приложения необходимо установить на компьютер Docker и утилиту docker-compose. Информация по установке доступна на официальном сайте документации, по ссылкам:
 - `https://docs.docker.com/get-docker/` 
 - `https://docs.docker.com/compose/install/`

Проект запускается в двух контейнерах. Первый - контейнер с Web-приложением, второй - контейнер с базой данных. Настройки базы данных экспортируются из переменных окружения, указанных в проекте. Чтобы задать свои значения нужно в корневой директории нужно создать файл .env следующего содержания: 

```
# имя базы данных
DB_NAME=postgres

# логин для подключения к базе данных
POSTGRES_USER=postgres 

# пароль для подключения к БД (установите свой)
POSTGRES_PASSWORD=postgres

# название сервиса (контейнера)
DB_HOST=db

# порт для подключения к БД
DB_PORT=5432
```

#### Запуск приложения

Для запуска приложения в терминале нужно перейти в корневую директорию проекта и выполнить команду:
 
 ```docker-compose up``` 

#### Первый запуск

Первый запуск приложения отличается от последующих запусков. Если вы запускаете приложение впервые вам нужно создать в базе данных структуру проекта(создать таблицы и связи между ними), собрать статические файлы в одну директорию и создать администратора приложения.

После выполнения команды ```docker-compose up``` в операционной системе запустятся два контейнера. С помощью команды ```docker ps -a``` нужно найти ID контейнера с именем ```infra_sp2_web```. 

Далее, с помощью команды ```sudo docker exec -it <container_ID> bash``` необходимо запустить терминал внутри контейнера с Web-приложением.

Создать необходимую структуру базы данных с помощью комманды:

```python manage.py migrate```

Выполнить сбор статичных файлов в одну директорию:

```python manage.py collectstatic```

Создать администратора приложения, следую инструкциям команды:

```python manage.py createsuperuser```

#### Загрузка тестовых данных

Для тестирования функционала проекта предусмотрен набор тестовых данных. Загрузить тестовые данные в базу можно из терминала контейнера Web-приложения, командой: 

```python manage.py loaddata fixtures.json```

![yamdb](https://github.com/blackwolfsm/yamdb_final/workflows/yamdb_final/badge.svg)
