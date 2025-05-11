export DJANGO_SETTINGS_MODULE=my_app.settings
python manage.py makemigrations my_app
python manage.py migrate
python manage.py runserver