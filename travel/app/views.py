from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .serializers import PostAddedSerializer
from .models import Post


@csrf_exempt
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostAddedSerializer


# Сохранение данных в БД
def create(request):
    if request.method == 'POST':
        post = Post()
        post.latitude = request.POST.get('latitude')
        post.longitude = request.POST.get('longitude')
        post.height = request.POST.get('height')
        post.title = request.POST.get('title')
        post.level = request.POST.get('level')
        post.author_id = request.POST.get('author_id')
        post.status = 'new'
        post.save()

        # Обработка загрузки изображений
        images = request.FILES.getlist('images')
        for image in images:
            post.images.create(image=image)

    return HttpResponseRedirect('/')


# Удаление данных из БД
def delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return HttpResponseRedirect('/')
