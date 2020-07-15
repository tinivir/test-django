init:
	docker-compose build
	docker-compose run web python manage.py migrate

run: 
	docker-compose up

test:
	docker-compose run web python manage.py test

loaddata:
	docker-compose run web python manage.py loaddata

createsuperuser:
	docker-compose run web python manage.py createsuperuser

makemigrations:
	docker-compose run web python manage.py makemigrations
