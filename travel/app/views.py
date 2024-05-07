from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import PostAddedSerializer
from .models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostAddedSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                # Ваш код для выполнения операции

                # Если операция выполнена успешно
                post_instance = serializer.save()
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Отправлено успешно",
                    "id": post_instance.id  # ID новой записи
                })

            except Exception as e:
                # Если произошла ошибка при выполнении операции
                return Response({
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": str(e)  # Причина ошибки
                })

        # Если запрос некорректен (например, нехватка полей)
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Bad Request"
        })

    def delete(self, request, *args, **kwargs):
        try:
            # Ваш код для удаления данных
            instance = self.get_object()
            self.perform_destroy(instance)

            # Если данные удалены успешно
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Успешно удалено"
            })

        except Post.DoesNotExist:
            # Если пост с указанным ID не найден
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Post not found"
            })

        except Exception as e:
            # Если произошла ошибка при удалении данных
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)  # Причина ошибки
            })