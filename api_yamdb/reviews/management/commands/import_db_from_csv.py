import csv

from django.core.management.base import BaseCommand
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)
from users.models import User

csv_file = {
    'static/data/category.csv': Category,
    'static/data/genre.csv': Genre,
    'static/data/titles.csv': Title,
    'static/data/users.csv': User,
    'static/data/review.csv': Review,
    'static/data/comments.csv': Comment,
}


class Command(BaseCommand):
    """
    Импорт csv в базу.
    Выполняется командой python manage.py import_db_from_csv.
    Необходимо запускать через терминал, находясь в соответствующей папке.
    """

    def _fix_table_fields(self, line):
        """
        Служебная функция.
        Исправляет таблицы базу.
        Дополняет экземплярами моделей.
        """
        try:
            if line.get('author'):
                line['author'] = User.objects.get(pk=line['author'])
            if line.get('review_id'):
                line['review'] = Review.objects.get(pk=line['review_id'])
            if line.get('title_id'):
                line['title'] = Title.objects.get(pk=line['title_id'])
            if line.get('category'):
                line['category'] = Category.objects.get(pk=line['category'])
            if line.get('genre'):
                line['genre'] = Genre.objects.get(pk=line['genre'])
        except Exception as error:
            print(f'Ошибка обнаружена в строке {line.get("id")}.\n'
                  f'Текст ошибки - {error}')
        return line

    def handle(self, *args, **options):
        """Основная функция."""
        for i in csv_file.items():
            path, model = i
            lines = 0
            successful = 0
            print(f'Создание модели {model.__name__}')
            with open(path, encoding='utf-8', mode='r') as file:
                csv_read = csv.DictReader(file)
                for line in csv_read:
                    lines += 1
                    line = self._fix_table_fields(line)
                    try:
                        model.objects.get_or_create(**line)
                        successful += 1
                    except Exception as error:
                        print(f'Ошибка обнаружена в строке {line.get("id")}.\n'
                              f'Текст ошибки - {error}')
            print(f'Создание модели {model.__name__} завершено. '
                  f'Всего строк: {lines}. Выполнено: {successful}.',
                  )
