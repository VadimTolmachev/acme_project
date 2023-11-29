"""...acme_project/brithday/models.py."""
from django.contrib.auth import get_user_model
# Подключаем базовую модель
from django.db import models
from django.urls import reverse

# Импортируется функция-валидатор.
from .validators import real_age

User = get_user_model()


class Birthday(models.Model):
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=20
    )
    last_name = models.CharField(
        'Фамилия',
        blank=True,
        help_text='Необязательное поле',
        max_length=20
    )
    birthday = models.DateField(
        'Дата рождения',
        validators=(real_age,)
    )
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)
    author = models.ForeignKey(
        User, verbose_name='Автор записи', on_delete=models.CASCADE, null=True
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
        )

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk})
