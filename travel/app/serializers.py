from rest_framework import serializers
from django.http import JsonResponse
import django_filters
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'email', 'phone')


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'image')


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('winter', 'spring', 'summer', 'autumn')


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ('latitude', 'longitude', 'height')


class PostAddedSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Первичные ключи пользователей
    images = serializers.ListField(child=serializers.ImageField())  # Список изображений
    coordinates = CoordinatesSerializer()  # Сериализатор координат
    level = LevelSerializer()  # Сериализатор уровня

    class Meta:
        model = Post
        fields = ('coordinates', 'level', 'title', 'user', 'images', 'created_at')

    def create(self, validated_data):
        # Добавление значения 'new' для поля 'status'
        validated_data['status'] = 'new'

        images_data = validated_data.pop('images')  # Удаление изображений из validated_data
        coordinates_data = validated_data.pop('coordinates')  # Удаление координат из validated_data
        level_data = validated_data.pop('level')  # Удаление уровня из validated_data
        user = validated_data.pop('user')  # Получение пользователя из validated_data

        post = Post.objects.create(user=user, **validated_data)  # Создание объекта поста

        for image_data in images_data:
            PostImage.objects.create(post=post, image=image_data)  # Создание объектов изображений

        Coordinates.objects.create(post=post, **coordinates_data)  # Создание объекта координат
        Level.objects.create(post=post, **level_data)  # Создание объекта уровня

        return post

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)  # Получение изображений из validated_data
        coordinates_data = validated_data.pop('coordinates', None)  # Получение координат из validated_data
        level_data = validated_data.pop('level', None)  # Получение уровня из validated_data

        for attr, value in validated_data.items():
            setattr(instance, attr, value)  # Обновление данных поста

        if coordinates_data:
            coordinates = instance.coordinates
            coordinates.latitude = coordinates_data.get('latitude', coordinates.latitude)
            coordinates.longitude = coordinates_data.get('longitude', coordinates.longitude)
            coordinates.height = coordinates_data.get('height', coordinates.height)
            coordinates.save()  # Обновление координат

        if level_data:
            level = instance.level
            level.winter = level_data.get('winter', level.winter)
            level.spring = level_data.get('spring', level.spring)
            level.summer = level_data.get('summer', level.summer)
            level.autumn = level_data.get('autumn', level.autumn)
            level.save()  # Обновление уровня

        if images_data:
            instance.images.all().delete()  # Удаление старых изображений
            for image_data in images_data:
                PostImage.objects.create(post=instance, image=image_data)  # Создание новых изображений

        instance.save()  # Сохранение изменений в посте
        return instance

    def delete(request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            return JsonResponse({'status': 200, 'message': 'Post deleted successfully'}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'status': 404, 'message': 'Post not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 500, 'message': str(e)}, status=500)
