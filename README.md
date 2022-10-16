бэкэнд часть для приложения для комплиментов

для запуска проекта команда:
```
docker-compose up --build -d
```

запускается на 8000 порту:
```
localhost:8000
```

сваггер:
```
localhost:8000/api/docs/
```

админка:
```
localhost:8000/admin/
```

создание юзера для админки:
```
docker-compose exec compliment_web python manage.py createsuperuser
```





