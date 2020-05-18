## Start

```shell script
docker-compose up --build
```

## Super user creation

```shell script
docker-compose run --rm backend python manage.py createsuperuser --username root --email admin@admin.com
```

## Admin
http://localhost:8000/admin/

Инлайн с опциями в вопросе будет показан после сохранения.

## Docs

http://localhost:8000/docs/


## Answer example
```json
{
  "user_id": 1,
  "poll": 1,
  "question_answers": [
      {
        "question": 1, 
        "text_answer": "text"
      },
      {
        "question": 2,
        "choice_answer": [3, 5]
      }
  ]
}
```
