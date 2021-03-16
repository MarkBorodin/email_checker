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
