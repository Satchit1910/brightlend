
# BrightLend

A Loan Management App for Bright Money

Built using Django REST Framework and PostgreSQL.
Hosted on Render.com (Both the web service and DB)

Base URL : [https://brightlend-pfmx.onrender.com](https://brightlend-pfmx.onrender.com).

### Run Locally

Clone the project

```bash
git clone https://github.com/Satchit1910/brightlend
```
Add .env file:
`DB_URL` = Add your database URL
`ALLOWED_HOSTS` = localhost
`DEBUG` = False/True

Run MakeMigrations and Migrate to generate the required Tables in the DB

```bash
python manage.py makemigrations
python manage.py migrate
```

Run the app :
```bash
python manage.py runserver
```



