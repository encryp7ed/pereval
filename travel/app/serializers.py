from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'second_name', 'middle_name', 'email', 'phone_number')


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'image')


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ('winter', 'spring', 'summer', 'autumn')


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()  # Сериализатор пользователя для поля автора
    images = PostImageSerializer(many=True)  # Сериализатор изображений для отношения ManyToMany
    coordinates = CoordinatesSerializer()

    class Meta:
        model = Post
        fields = ('id', 'coordinates', 'name', 'author', 'images', 'created_at')
