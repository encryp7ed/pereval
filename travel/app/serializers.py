from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'email', 'phone_number')


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


class PostAddedSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer()  # Сериализатор пользователя для поля автора
    images = PostImageSerializer(many=True)  # Сериализатор изображений для отношения ManyToMany
    coordinates = CoordinatesSerializer()
    level = LevelSerializer()

    class Meta:
        model = Post
        fields = ('id', 'coordinates', 'level', 'title', 'author', 'images', 'created_at')
