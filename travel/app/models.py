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
    STATUS_CHOICES = [
        ('new', 'New'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # широта
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # долгота
    height = models.DecimalField(max_digits=6, decimal_places=2)  # высота
    title = models.CharField(max_length=100)  # Название
    # В случае удаления пользователя оставляем запись
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания
    images = models.ManyToManyField('PostImage')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')  # Статус модерации

    objects = models.Manager()


class PostImage(models.Model):
    # Сохраняем ссылки на изображения
    image = models.ImageField(upload_to='images/')

    objects = models.Manager()
