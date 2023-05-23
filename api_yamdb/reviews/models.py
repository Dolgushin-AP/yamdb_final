from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import LIMIT, MAX_LIMIT_VALUE, MIN_LIMIT_VALUE
from users.models import User


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг категории',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name='Слаг жанра',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название произведения',
    )
    year = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(
                0,
                message='Год не может быть отрицательным'
            ),
            MaxValueValidator(
                int(datetime.now().year),
                message='Год не может быть больше текущего'
            )
        ],
        db_index=True,
        verbose_name='Год',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        related_name='title',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='title',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        related_name='reviews',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        verbose_name='Название произведения',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[
            MaxValueValidator(MAX_LIMIT_VALUE, 'Максимальное значение — 10'),
            MinValueValidator(MIN_LIMIT_VALUE, 'Минимальное значение — 1')
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        default_related_name = 'reviews'
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_name_review'
            )
        ]

    def __str__(self):
        return self.text[LIMIT]


class Comment(models.Model):
    """Модель комментариев"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Комментарий'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий к отзыву'

    def __str__(self) -> str:
        return self.text[LIMIT]
