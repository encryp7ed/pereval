from django.db import models


class Post(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # широта
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # долгота
    height = models.DecimalField(max_digits=6, decimal_places=2)  # высота
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='images/')  # Сохраняем путь к изображению
