# Foodgram - graduate project

![Foodgram workflow status](https://github.com/evgeny81d/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Foodgram allows users to publish recipes, subscribe to other users,
add recipes to favorites and shopping cart, download list of products from 
shopping cart to buy everything and start cooking.


[Demo web site](http://158.160.44.11)


# Technology stack

* Python 3.7
* Django 3.2
* Django REST framework 3.14
* Django filter 22.1
* Gunicorn 20.1
* Nginx 1.19
* Postgresql 13
* Docker


# How it works

Foodgram runs in docker containers and consists of four main components:
* Frontend - nice looking frontend provided by [Yandex.Practicum](https://practicum.yandex.ru)
* Backend - django web application with API and admin site
* Database - postgresql database to store all project data
* Nginx - the hardworker who manages frontend, backend and database interaction

# How to install and run on local host

Prerequisites: git, docker and docker-compose should be already installed

## Clone repository and create file with secrets

1. Clone repository
```sh
# Clone repository
git clone https://github.com/evgeny81d/foodgram-project-react
```

2. Create `.env` file in `foodgram-project-react/infra/` directory with 
following content 
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<your db name>
POSTGRES_USER=<your postgres user name>
POSTGRES_PASSWORD=<your postres user password>
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<your django secret key>
```

## Run the project

```sh
# Go to project directory
cd foodgram-project-react/infra/

# Start the project
sudo docker-compose up --build -d

# Run migrations in backend container
sudo docker exec -it infra_backend_1 python manage.py migrate

# Collect static files in backend container
sudo docker exec -it infra_backend_1 python manage.py collectstatic --no-input

# Create supseruser
sudo docker exec -it infra_backend_1 python manage.py createsuperuser
```


Now foodgram homepage is avialable here: http://localhost

Admin site: http://localhost/admin/

API docs: http://localhost/api/docs/


## Stop the project

```sh
# Stop and delete all data
sudo docker-compose down -v


# Stop and persist data
sudo docker-compose stop

# Start again
sudo docker-compose start
```

# How to install virtual environment and run pytest

```sh
# Go project directory
cd foodgram-project-react

# Install Python 3.7 virtual environment
python3.7 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Go to backend directory
cd backend

# Install requirements
pip install -r requirements.txt --upgrade pip

# Go back to project direcotory
cd ..

# Run pytest
pytest
```
