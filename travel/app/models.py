from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, error_messages={
            'unique': _('A user with that email already exists.'),  # Выводим сообщение об ошибке на языке пользователя
        },)
    phone_number = models.CharField(max_length=15, unique=True, error_messages={
        'unique': _('A user with that phone number already exists.'),
    })

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"


class Post(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # широта
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # долгота
    height = models.DecimalField(max_digits=6, decimal_places=2)  # высота
    title = models.CharField(max_length=100)  # Название
    # В случае удаления пользователя оставляем запись
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания


class PostImage(models.Model):
    # Привязываем изображений к конкретной записи
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    # Сохраняем путь к изображению
    image = models.ImageField(upload_to='images/')
