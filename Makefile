local-run:
	python manage.py makemigrations --noinput
	python manage.py migrate --noinput
	python manage.py runserver

mig:
	python manage.py makemigrations --noinput
	python manage.py migrate --noinput

worker:
	celery -A config worker -E -l info

beat:
	celery -A config.settings beat -E -l info
