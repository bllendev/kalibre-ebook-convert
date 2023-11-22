web: gunicorn ebook_convert.wsgi
release: python manage.py migrate && python manage.py collectstatic --noinput
