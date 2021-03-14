# INSTALL_APP


### Setup

clone repository:
```
git clone https://github.com/MarkBorodin/email_checker.git
```
move to folder "pdf_generator":
```
cd email_checker
```

to install the required libraries, run on command line:
```
pip install -r requirements.txt
```

you shout make migration:
```
python manage.py migrate
```

### run app


to work you need to create a superuser. Run and follow the prompts:

```
python manage.py createsuperuser
```

to start the server - run:

```
python manage.py runserver
```

and follow the link:

```
http://127.0.0.1:8000/admin
```


### or you can run this in docker

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


### check email existence


"Warnings and Disclaimers
While this process will get you up and running, you need to be aware of the following risks:

Do this too much and you will get put on a naughty list (e.g. Spamhaus), especially if you are using a dynamic IP address from your ISP.
B2C addresses: this does not work very well against the big boys who have their own procedures and spam rules (e.g.hotmail and yahoo).
Incorrect results: some mail servers will give you incorrect results, for instance catch-all servers, which will accept all incoming email addresses, often forwarding incoming emails to a central mailbox. Yahoo addresses displays this catch-all behavior.
This script on its own is not enterprise grade email verification; you will not be able to process millions of addresses with it."
#### source: https://www.scottbrady91.com/Email-Verification/Python-Email-Verification-Script