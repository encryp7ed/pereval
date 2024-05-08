# Документация REST API

## Эндпоинты
***Получение списка всех постов***

`GET /posts/`

Этот эндпоинт позволяет получить список всех постов.

***Параметры запроса***

Отсутствуют

***Ответ***

```json
[
    {
        "id": 1,
        "title": "Заголовок поста 1",
        "user": 1,
        "images": ["image1.jpg", "image2.jpg"],
        "coordinates": {"latitude": 12.345, "longitude": 67.890},
        "level": {"winter": "easy", "summer": "moderate"},
        "created_at": "2024-05-08T12:00:00Z"
    },
    {
        "id": 2,
        "title": "Заголовок поста 2",
        "user": 2,
        "images": ["image3.jpg", "image4.jpg"],
        "coordinates": {"latitude": 23.456, "longitude": 78.901},
        "level": {"winter": "moderate", "summer": "difficult"},
        "created_at": "2024-05-09T13:00:00Z"
    },
    ...
]
```
