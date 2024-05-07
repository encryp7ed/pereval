from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, error_messages={
            'unique': _('A user with that email already exists.'),  # Выводим сообщение об ошибке на языке пользователя
        },)
    phone = models.CharField(max_length=15, unique=True, error_messages={
        'unique': _('A user with that phone number already exists.'),
    })

    objects = models.Manager()

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name} {self.email} {self.phone}'


class Level(models.Model):
    winter = models.CharField(max_length=255)
    spring = models.CharField(max_length=255)
    summer = models.CharField(max_length=255)
    autumn = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return f'{self.winter} {self.spring} {self.summer} {self.autumn}'


class Coordinates(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)  # широта
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)  # долгота
    height = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # высота

    objects = models.Manager()

    def __str__(self):
        return f'{self.latitude} {self.longitude} {self.height}'


class Post(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),  # Добавлено на проверку
        ('pending', 'Pending'),  # На проверке у модерации
        ('accepted', 'Accepted'),  # Пост успешно прошел проверку модерации
        ('rejected', 'Rejected'),  # Пост неуспешно прошел проверку модерации
    ]

    coordinates = models.ManyToManyField('Coordinates')
    title = models.CharField(max_length=100)  # Название
    # В случае удаления пользователя оставляем запись
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания
    images = models.ManyToManyField('PostImage', related_name='posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')  # Статус модерации
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)

    objects = models.Manager()


class PostImage(models.Model):
    pereval = models.ForeignKey(Post, related_name='post_images', on_delete=models.CASCADE)
    # Сохраняем ссылки на изображения
    image = models.ImageField(upload_to='images/')

    objects = models.Manager()

    def __str__(self):
        return f'{self.image}'
