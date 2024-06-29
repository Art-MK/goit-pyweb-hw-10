#!/bin/bash

project_name="quotes_project"
username="admin"
password="admin"

docker compose up -d

python ./$project_name/manage.py makemigrations
python ./$project_name/manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('$username', 'admin@example.com', '$password')" | python ./$project_name/manage.py shell

echo "Username admin"
echo "Password admin"

pushd $project_name
python manage.py runserver