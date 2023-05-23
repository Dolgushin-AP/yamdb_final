## yamdb_final
yamdb_final
## Проект: Настройка CI/CD с помощью GitHub Actions для YaMDb.
[![YaMDb workflow](https://github.com/Dolgushin-AP/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/Dolgushin-AP/yamdb_final/actions/workflows/yamdb_workflow.yml)

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.


### Предварительные требования:
Установить и запустить Docker Desktop

### Запуск проекта:

*Примечание:* должен быть установлен Docker.

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Dolgushin-AP/yamdb_final.git
```
```
cd yamdb_final/infra
```

Запустить контейнеры:
```
docker compose up -d --build
```

Заполнить .env по шаблону:
```
nano .env
```
```
DB_ENGINE=django.db.backends.postgresql
```
DB_NAME=postgres
```
POSTGRES_USER=postgres
```
POSTGRES_PASSWORD=postgres
```
DB_HOST=db
```
DB_PORT=5432
```

Запустить docker-compose:
```
docker-compose up
```

Выполнить команды:
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
```

Создать резервную копию базы данных:
```
docker-compose exec web python manage.py dumpdata > fixtures.json
```

Прежде чем войти в админку, необходимо создать суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
