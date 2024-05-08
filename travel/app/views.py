from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PostAddedSerializer
from .models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostAddedSerializer
    filter_backends = [DjangoFilterBackend]  # Добавляем поиск по фильтрам
    filterset_fields = ['user__email']  # Поля для фильтрации

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

    # Получаем информацию о перевале по его id, включая статус ее модерации
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)  # Вся информация об объекте
            return Response(serializer.data)

        except Post.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Post not found"
            })

        except Exception as e:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            })

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            if instance.status == 'new':
                # Убедимся, что поля ФИО, адреса почты и номера телефона не меняются
                if 'user' in serializer.validated_data or 'coordinates' in serializer.validated_data or 'level' in serializer.validated_data:
                    return Response({
                        "status": '0',
                        "message": "Вы не можете изменить поля user, coordinates или level"
                    })
                else:
                    serializer.save()
                    return Response({
                        "status": '1',
                        "message": "Пост успешно обновлен"
                    })
            else:
                return Response({
                    "status": '0',
                    "message": "Пост не имеет статус 'new' и не может быть обновлен"
                })
        else:
            return Response(serializer.errors, status='0')
