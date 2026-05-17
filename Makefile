local-run:
	python manage.py makemigrations --noinput
	python manage.py migrate --noinput
	python manage.py runserver

mig:
	python manage.py makemigrations --noinput
	python manage.py migrate --noinput
