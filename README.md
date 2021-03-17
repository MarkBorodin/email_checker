# INSTALL_APP


### Setup


clone repository:
```
git clone https://github.com/MarkBorodin/email_checker.git
```

move to folder "email_checker":
```
cd email_checker
```


### run this in docker

run:

```
docker-compose up --build
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic
```

follow the link:
```
http://127.0.0.1/admin/
```


### Finish



### API

to use api, you need to get a token:

```
http://localhost/api/v1/token/
```

After that, you need to use this token in headers in requests.

```
(From the documentation:
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8000/api/some-protected-view/)
```

Request example:

```
POST: http://localhost/api/v1/email_check/
body:
 {
"email": "example@gmail.com"
}
```

Response example:

```
{
    "email": "example@gmail.com",
    "valid": true,
    "accessible": false,
    "catchall": false
}
```
