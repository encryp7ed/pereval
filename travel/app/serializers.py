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


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()  # Сериализатор пользователя для поля автора
    images = PostImageSerializer(many=True)  # Сериализатор изображений для отношения ManyToMany

    class Meta:
        model = Post
        fields = ('id', 'latitude', 'longitude', 'height', 'name', 'author', 'images', 'created_at')