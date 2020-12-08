from datetime import datetime as dt

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=150,
                            unique=True)
    slug = AutoSlugField(populate_from='name', primary_key=True)


class Genre(models.Model):
    name = models.CharField(verbose_name='Название жанра', max_length=150,
                            unique=True)
    slug = AutoSlugField(populate_from='name', primary_key=True)


class Title(models.Model):
    name = models.CharField(verbose_name='Название произведения',
                            max_length=200)
    year = models.IntegerField(
        verbose_name='Год публикации', default=0, db_index=True,
        validators=[MaxValueValidator(
            dt.now().year, message='Год не может быть больше текущего')]
    )
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 null=True, blank=True,
                                 on_delete=models.SET_DEFAULT,
                                 related_name='titles', default=None)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр', blank=True,
                                   related_name='titles', default=None)
    description = models.TextField(default='', verbose_name='Описание')

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title, verbose_name='Оцениваемое произведение',
                              on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(verbose_name='Текст ревью')
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(
            1, message='Ваша оценка не может быть меньше 1'
        ),
                    MaxValueValidator(
            10, message='Ваша оценка не может быть больше 10')]
        )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, verbose_name='Автор оценки',
                               on_delete=models.CASCADE,
                               related_name='reviews')

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор комментария',
                               on_delete=models.CASCADE,
                               related_name='comments')
    review = models.ForeignKey(Review, verbose_name='Ревью для комментария',
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True,
                                    db_index=True)
